from classes.AuxAstInfo import AuxAstInfo
import re


class Prettifier:
    _minified = None
    _prettified = None
    _prettified_is_postprocessed = None
    _last_cst = None
    _indent = None
    _context_stack = None  # used to distinguish different contexts while parsing and interpreting the same lexemes

    def __init__(self):
        """
        Constructor of Prettyfier
        """
        self._last_cst = ""
        self._minified = ""
        self._prettified = ""
        self._prettified_is_postprocessed = False
        self._indent = 0
        self._context_stack = []

    def minify(self, ast_info: AuxAstInfo):
        """
        Builds up a minified representation of the parsed fpl file during the parsing process
        :param ast_info: info about the parsed item
        :return: None
        """
        if self._prettified.find("ProceedingResults(p: +") > -1:
            # print("")
            pass
        #  print(self._context_stack, self._minified[-50:])
        if isinstance(ast_info.cst, str):
            if ast_info.rule == "Comment":
                self._append_indented(ast_info.cst)
            elif ast_info.rule == "CommentWhitespaceList":
                pass
            elif ast_info.rule == "LongComment":
                self._append_indented(ast_info.cst, linebreaks=2)
            elif ast_info.rule == "IW":
                pass
            elif ast_info.rule == "CW":
                pass
            elif ast_info.rule == "Entity":
                self._last_cst = ast_info.cst
            elif ast_info.rule == "Comma":
                self._last_cst = ","
                if self.is_parsing_context(["dolinebreaks", "paren"]):
                    self._append_indented(",")
                else:
                    self._append(", ")
            elif ast_info.rule == "Colon":
                self._last_cst = ":"
                # last word:
                if self.__last_word() in ["con", "conclusion", "pre", "premise"]:
                    self._append_indented(": ", strip=True)
                elif self.is_parsing_context(["case", "dolinebreaks", "paren", "aftercase"]):
                    self._append(":")
                    self._increase_indent()  # increase indent after the case
                    self._append_indented("")
                else:
                    self._append(": ")
            elif ast_info.rule == "ColonEqual":
                self._last_cst = ":="
                self._append(" := ")
            elif ast_info.rule == "else":
                self._append("else")
                if self.is_parsing_context(["case", "dolinebreaks", "paren"]):
                    # remember that we are after a case context
                    self.push_context("aftercase")
            elif ast_info.rule == "LeftBracket":
                self._last_cst = "["
                self._append("[")
                self.push_context("nolinebreak")
            elif ast_info.rule == "LeftParen":
                self._last_cst = "("
                self.push_context("paren")
                # line break if we are in the context of a starting compound predicate, ex., "and (...."
                self._open_left_block("(", linebreak=self.is_parsing_context(["dolinebreaks", "paren"]))
            elif ast_info.rule == "LeftBrace":
                self._last_cst = "{"
                self._open_left_block("{", linebreak=True)
            elif ast_info.rule == "RightBracket":
                self._last_cst = "]"
                self._append("]")
                self.pop_context(["nolinebreak"])
            elif ast_info.rule == "RightParen":
                self._last_cst = ")"
                # line break if we are in the context of a starting compound predicate, ex., "and (...."
                self._close_right_block(")", linebreak=self.is_parsing_context(["dolinebreaks", "paren"]))
                if self.is_parsing_context(["paren"]):
                    self.pop_context(["paren"])
                else:
                    # missing closing paren detected
                    pass
            elif ast_info.rule == "RightBrace":
                self._last_cst = "}"
                self._close_right_block("}", linebreak=True)
            elif ast_info.rule == "SW":
                self._last_cst = ""
                self._append(" ", significant_whitespaces=True)
            elif ast_info.rule == "To":
                self._last_cst = "->"
                self._append(" -> ")
            elif ast_info.rule == "tpl" and self._last_cst[0:3] == ast_info.cst:
                self._last_cst = ast_info.cst
            else:
                if self._last_cst == ast_info.cst:
                    # prevent repeating of the parsed text because of nested productions
                    pass
                else:
                    self._last_cst = ast_info.cst
                    # replace long versions by short versions
                    if ast_info.cst in ["and", "or", "impl", "iif", "xor", "not", "all", "ex", "loop", "range"]:
                        self._replace_long_by_short(ast_info.cst, ast_info.cst, line_separator="", indent=False)
                        self.push_context("dolinebreaks")
                    elif ast_info.cst == "assert":
                        self._append_indented(ast_info.cst)
                        self._increase_indent()  # increase indent after an assert keyword
                        self._append_indented("")
                    elif ast_info.cst == "case":
                        self._replace_long_by_short(ast_info.cst, ast_info.cst, line_separator="", indent=False)
                        self.push_context("case")
                        self.push_context("dolinebreaks")
                    elif ast_info.cst in ["assume", "ass"]:
                        if "insideproof" in self._context_stack:
                            self._replace_long_by_short("ass", ast_info.cst, line_separator="", indent=False)
                        else:
                            self._replace_long_by_short("ass", ast_info.cst)
                    elif ast_info.cst in ["axiom", "ax"]:
                        self._replace_long_by_short("ax", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["class", "cl"]:
                        self._replace_long_by_short("cl", ast_info.cst)
                    elif ast_info.cst in ["conclusion", "con"]:
                        self._replace_long_by_short("con", ast_info.cst)
                        self._increase_indent()  # increase indent after an conclusion keyword
                        self._append_indented("")
                    elif ast_info.cst in ["conjecture", "conj"]:
                        self._replace_long_by_short("conj", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["corollary", "corr"]:
                        self._replace_long_by_short("cor", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["function", "func"]:
                        if self._prettified.strip()[-1] in [":", "+", "*"]:
                            # in the context of a variable declaration of type 'func' there will be no break
                            self._replace_long_by_short("func", ast_info.cst, line_separator="", indent=False)
                        else:
                            self._replace_long_by_short("func", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["inference", "inf"]:
                        self._replace_long_by_short("inf", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["lemma", "lem"]:
                        self._replace_long_by_short("lem", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["mandatory", "mand"]:
                        self._replace_long_by_short("mand", ast_info.cst)
                    elif ast_info.cst in ["object", "obj"]:
                        self._replace_long_by_short("obj", ast_info.cst, line_separator="", indent=False)
                    elif ast_info.cst in ["optional", "opt"]:
                        self._replace_long_by_short("opt", ast_info.cst)
                    elif ast_info.cst in ["predicate", "pred"]:
                        if self._prettified.strip()[-1] in [":", "+", "*"]:
                            # in the context of a variable declaration of type 'pred' there will be no break
                            self._replace_long_by_short("pred", ast_info.cst, line_separator="", indent=False)
                        else:
                            self._replace_long_by_short("pred", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["premise", "pre"]:
                        if "insideproof" in self._context_stack:
                            self._replace_long_by_short("pre", ast_info.cst, line_separator="", indent=False)
                        else:
                            self._replace_long_by_short("pre", ast_info.cst)
                            self._increase_indent()  # increase indent after an premise keyword
                            self._append_indented("")
                    elif ast_info.cst in ["postulate", "post"]:
                        self._replace_long_by_short("post", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["proof", "prf"]:
                        self._replace_long_by_short("prf", ast_info.cst, line_separator="\n\n")
                        self.push_context("insideproof")
                    elif ast_info.cst in ["proposition", "prop"]:
                        self._replace_long_by_short("prop", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["return", "ret"]:
                        self._replace_long_by_short("ret", ast_info.cst)
                    elif ast_info.cst in ["revoke", "rev"]:
                        self._replace_long_by_short("rev", ast_info.cst)
                    elif ast_info.cst in ["syntax", "syn"]:
                        self._replace_long_by_short("syn", ast_info.cst)
                    elif ast_info.cst in ["template", "tpl"]:
                        self._replace_long_by_short("tpl", ast_info.cst, line_separator="", indent=False)
                    elif ast_info.cst in ["theorem", "thm"]:
                        self._replace_long_by_short("thm", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["theory", "th"]:
                        self._replace_long_by_short("th", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["undefined", "undef"]:
                        self._replace_long_by_short("undef", ast_info.cst, line_separator="", indent=False)
                    elif ast_info.cst == "uses":
                        self._replace_long_by_short(ast_info.cst, ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst == "else":
                        pass  # this cst is handled above as a rule
                    else:
                        self._replace_long_by_short(ast_info.cst, ast_info.cst, line_separator="",
                                                    indent=False)
        else:
            if ast_info.rule in ["AssertionStatement", "ConclusionBlock", "PremiseBlock"]:
                self._decrease_indent()
            elif ast_info.rule in ["ConditionFollowedByResult", "DefaultResult"]:
                self._decrease_indent()
                self._append_indented("")
                self.pop_context(["aftercase"])  # remove the after case flag again
            elif ast_info.rule in ["StatementList"]:
                if self.is_parsing_context(["case", "dolinebreaks", "paren"]):
                    self._decrease_indent()
                    self._append_indented("")
            elif ast_info.rule == "CaseStatement":
                self.pop_context(["case", "dolinebreaks"])  # remove the "case", "dolinebreaks" flag from the context
            elif ast_info.rule in ["CompoundPredicate", "RangeStatement", "LoopStatement"]:
                self.pop_context(["dolinebreaks"])  # remove the "dolinebreaks" flag from the context
            elif ast_info.rule == "ExtensionHeader":
                self._increase_indent()
                self._prettified = self._prettified[:-5] + ":ext\n" + "\t" * self._indent
            elif ast_info.rule == "ExtensionTail":
                self._decrease_indent()
                self._prettified = self._prettified[:-6] + "\n" + "\t" * self._indent + ":end\n"
            elif ast_info.rule == "Predicate":
                if self.is_parsing_context(["case", "dolinebreaks", "paren"]):
                    # remember that we are after a case context
                    self.push_context("aftercase")
            elif ast_info.rule == "ProofArgument":
                self._append_indented("")
            elif ast_info.rule == "Proof":
                self.pop_context(["insideproof"])
            elif ast_info.rule in ["VariableSpecification", "Statement"]:
                # line break after each VariableSpecification in the prettyfied version
                self._prettified = self._prettified + "\n" + "\t" * self._indent

    def __last_word(self):
        if len(self._prettified.strip()) > 0:
            return self._prettified.strip().split()[-1]
        else:
            return ""

    def _append_to_minified(self, text: str, significant_whitespaces=False):
        if not significant_whitespaces:
            text = text.strip()
        if text[0:2] == "//" or text[0:2] == "/*":
            # ignore comments
            pass
        else:
            self._minified += text

    def _append(self, text: str, strip=False, significant_whitespaces=False):
        self._append_to_minified(text, significant_whitespaces)
        if strip:
            self._prettified = self._prettified.strip()
        self._prettified += text

    def _append_indented(self, text: str, linebreaks=1, strip=False, significant_whitespaces=False):
        self._append_to_minified(text, significant_whitespaces)
        if strip:
            self._prettified = self._prettified.strip()
        self._prettified += text + "\n" * linebreaks + "\t" * self._indent

    def get_prettified(self):
        """
        Returns the current prettified version of the FPL code
        :return: A prettified version of the FPL code
        """
        if self._prettified_is_postprocessed:
            return self._prettified
        else:
            self._prettyfied_post_process()
            return self._prettified

    def get_minified(self):
        """
        Returns the current minified version of the FPL code
        :return: A minified version of the FPL code
        """
        if len(self._context_stack) > 0:
            # the _context stack has to be empty after the prettyfying process, otherwise, something is wrong
            raise AssertionError("Context stack not empty after minifying the code")
        return self._minified

    def _close_right_block(self, paren: str, linebreak=False):
        if linebreak:
            self._indent -= 1
            if self._indent < 0:
                # to many closing parentheses detected
                self._indent = 0
            self._append_indented("")
            self._append(paren)
        else:
            self._append(paren)
        # add an extra line break after "}"
        if paren == "}":
            self._append_indented("")

    def _open_left_block(self, paren: str, linebreak=False):
        if linebreak:
            self._append_indented("")
            self._append(paren)
            self._append("\n")
            self._indent += 1
            self._append_indented("", linebreaks=0)
        else:
            self._append(paren)

    def _replace_long_by_short(self, short: str, original: str, line_separator="\n", indent=True):
        self._minified += short
        self._prettified += line_separator
        if indent:
            self._prettified += "\t" * self._indent
        self._prettified += original

    def _increase_indent(self):
        """
        Increases the current indentation of self
        :return: None
        """
        self._indent += 1

    def _decrease_indent(self):
        """
        Decreases the current indentation of self
        :return: None
        """
        if self._indent == 0:
            raise AssertionError("Cannot decrease indentation any more")
        else:
            self._indent -= 1

    def _prettyfied_post_process(self):
        # remove all spaces if they are proceeded by "\t"
        length = 0
        while len(self._prettified) != length:
            length = len(self._prettified)
            self._prettified = self._prettified.replace("\t ", "\t")
        # remove all empty lines after a brace "{" opening a new block
        self._prettified = re.sub('{\n\t*\n', '{\n', self._prettified)

        lines = self._prettified.split("\n")
        prettyfied_lines = []
        i = 0
        while i < len(lines) - 1:
            line = lines[i].strip()
            next_line = lines[i + 1].strip()
            if line == next_line == "":
                # replace double empty lines by single one
                prettyfied_lines.append(lines[i])
                i += 1
            elif line == "" and next_line == "}":
                # replace empty lines followed by "}" by "}"
                prettyfied_lines.append(lines[i + 1])
                i += 1
            else:
                prettyfied_lines.append(lines[i])
            i += 1
        self._prettified = "\n".join(prettyfied_lines)

    def is_parsing_context(self, pars: list):
        """
        Check if the current parsing context ends with some given flags
        :param pars: list of keys
        :return: True, iif the context's tail corresponds to the keys in their order
        """
        if len(self._context_stack) < len(pars):
            return False
        else:
            is_context = True  # assume the context is there
            pos = len(self._context_stack) - len(pars)
            for x in pars:
                is_context = is_context and (x == self._context_stack[pos])
                if not is_context:
                    break
                pos += 1
            return is_context

    def push_context(self, key):
        """
        Pushes the parsing context on a stack
        :param key: key of the context
        :return: None
        """
        self._context_stack.append(key)

    def pop_context(self, pars: list):
        """
        Pops the last context from the stack.
        :param pars: a context (list) assumed to be at the tail of the stack. Raises an AssertionError if not
        :return: None
        """
        if len(self._context_stack) >= len(pars):
            if not self.is_parsing_context(pars):
                raise AssertionError(
                    "Got context " + str(self._context_stack[-len(pars):]) + ", expected " + str(list(pars)))
            else:
                self._context_stack = self._context_stack[:len(self._context_stack) - len(pars)]
        else:
            raise AssertionError("Got context " + str([]) + ", expected " + str(list(pars)))

    def get_context(self):
        return self._context_stack
