from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxContext import AuxContext
import re
import configparser
import os
from ide.Settings import Settings


class AuxPrettifier:

    def __init__(self):
        """
        Constructor of Prettifier
        """
        self._last_cst = ""
        self._minified = ""
        self._prettified = ""
        self._prettified_is_postprocessed = False
        self._indent = 0
        self._context = AuxContext()
        self.config = configparser.RawConfigParser()
        path_to_config = os.path.realpath(os.path.join(os.path.dirname(__file__) + "../../../ide/config.ini"))
        self.config.read(path_to_config)

    def minify(self, ast_info: AuxAstInfo):
        """
        Builds up a minified representation of the parsed fpl file during the parsing process
        :param ast_info: info about the parsed item
        :return: None
        """
        if isinstance(ast_info.cst, str):
            if ast_info.rule == "Comment":
                self._append_indented(ast_info.cst, ignore_minified=True)
            elif ast_info.rule == "CommentWhitespaceList":
                pass
            elif ast_info.rule == "LongComment":
                self._append_indented(ast_info.cst, linebreaks=2, ignore_minified=True)
            elif ast_info.rule == "IW":
                pass
            elif ast_info.rule == "CW":
                pass
            elif ast_info.rule == "Entity":
                self._last_cst = ast_info.cst
            elif ast_info.rule == "Comma":
                self._last_cst = ","
                if self._context.is_parsing_context([AuxContext.dolinebreaks, AuxContext.paren]):
                    self._append_indented(",")
                else:
                    self._append(", ")
            elif ast_info.rule == "Colon":
                self._last_cst = ":"
                # last word:
                if self.__last_word() in ["con", "conclusion", "pre", "premise"]:
                    self._append_indented(": ", strip=True)
                elif self._context.is_parsing_context(
                        [AuxContext.case, AuxContext.dolinebreaks, AuxContext.paren, AuxContext.aftercase]):
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
                if self._context.is_parsing_context([AuxContext.case, AuxContext.dolinebreaks, AuxContext.paren]):
                    # remember that we are after a case context
                    self._context.push_context(AuxContext.aftercase)
            elif ast_info.rule == "LeftBracket":
                self._last_cst = "["
                self._append("[")
                self._context.push_context(AuxContext.nolinebreak)
            elif ast_info.rule == "LeftParen":
                self._last_cst = "("
                self._context.push_context(AuxContext.paren)
                # line break if we are in the context of a starting compound predicate, ex., "and (...."
                self._open_left_block("(", linebreak=self._context.is_parsing_context(
                    [AuxContext.dolinebreaks, AuxContext.paren]))
            elif ast_info.rule == "LeftBrace":
                self._last_cst = "{"
                self._open_left_block("{", linebreak=True)
            elif ast_info.rule == "RightBracket":
                self._last_cst = "]"
                self._append("]")
                self._context.pop_context([AuxContext.nolinebreak])
            elif ast_info.rule == "RightParen":
                self._last_cst = ")"
                # line break if we are in the context of a starting compound predicate, ex., "and (...."
                self._close_right_block(")", linebreak=self._context.is_parsing_context(
                    [AuxContext.dolinebreaks, AuxContext.paren]))
                if self._context.is_parsing_context([AuxContext.paren]):
                    self._context.pop_context([AuxContext.paren])
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
                    if ast_info.cst in ["and", "or", "impl", "iif", "xor", "not", "all", "ex"]:
                        self._replace_long_by_short(ast_info.cst, ast_info.cst, line_separator="", indent=False)
                        one_line_predicates = self.config.get(Settings.section_codereform,
                                                              Settings.option_codereform_1linecomppred)
                        if one_line_predicates == "False":
                            self._context.push_context(AuxContext.dolinebreaks)
                    elif ast_info.cst in ["loop", "range"]:
                        self._replace_long_by_short(ast_info.cst, ast_info.cst, line_separator="", indent=False)
                        self._context.push_context(AuxContext.dolinebreaks)
                    elif ast_info.cst == "assert":
                        self._append_indented(ast_info.cst)
                        self._increase_indent()  # increase indent after an assert keyword
                        self._append_indented("")
                    elif ast_info.cst == "cases":
                        self._replace_long_by_short(ast_info.cst, ast_info.cst, line_separator="", indent=False)
                        self._context.push_context(AuxContext.case)
                        self._context.push_context(AuxContext.dolinebreaks)
                    elif ast_info.cst in ["assume", "ass"]:
                        if AuxContext.insideproof in self._context.get_context():
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
                        if "insideproof" in self._context.get_context():
                            self._replace_long_by_short("pre", ast_info.cst, line_separator="", indent=False)
                        else:
                            self._replace_long_by_short("pre", ast_info.cst)
                            self._increase_indent()  # increase indent after an premise keyword
                            self._append_indented("")
                    elif ast_info.cst in ["postulate", "post"]:
                        self._replace_long_by_short("post", ast_info.cst, line_separator="\n\n")
                    elif ast_info.cst in ["ProofArgument", "prf", "proof"]:
                        self._replace_long_by_short("prf", ast_info.cst, line_separator="\n\n")
                        self._context.push_context(AuxContext.insideproof)
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
                self._context.pop_context([AuxContext.aftercase])  # remove the after case flag again
            elif ast_info.rule in ["StatementList"]:
                if self._context.is_parsing_context([AuxContext.case, AuxContext.dolinebreaks, AuxContext.paren]):
                    self._decrease_indent()
                    self._append_indented("")
            elif ast_info.rule == "CaseStatement":
                # remove the "case", "dolinebreaks" flag from the context
                self._context.pop_context([AuxContext.case, AuxContext.dolinebreaks])
            elif ast_info.rule == "CompoundPredicate":
                one_line_predicates = self.config.get(Settings.section_codereform,
                                                      Settings.option_codereform_1linecomppred)
                if one_line_predicates == "False":
                    # remove the "dolinebreaks" flag from the context
                    self._context.pop_context([AuxContext.dolinebreaks])
            elif ast_info.rule in ["RangeStatement", "LoopStatement"]:
                self._context.pop_context([AuxContext.dolinebreaks])  # remove the "dolinebreaks" flag from the context
            elif ast_info.rule == "ExtensionHeader":
                self._increase_indent()
                self._prettified = self._prettified[:-5] + ":ext\n" + "\t" * self._indent
            elif ast_info.rule == "ExtensionTail":
                self._decrease_indent()
                self._prettified = self._prettified[:-6] + "\n" + "\t" * self._indent + ":end\n"
            elif ast_info.rule == "Predicate":
                if self._context.is_parsing_context([AuxContext.case, AuxContext.dolinebreaks, AuxContext.paren]):
                    # remember that we are after a case context
                    self._context.push_context(AuxContext.aftercase)
            elif ast_info.rule == "ProofArgument":
                self._append_indented("")
            elif ast_info.rule == "Proof":
                self._context.pop_context([AuxContext.insideproof])
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
        self._minified += text

    def _append(self, text: str, strip=False, significant_whitespaces=False):
        self._append_to_minified(text, significant_whitespaces)
        if strip:
            self._prettified = self._prettified.strip()
        self._prettified += text

    def _append_indented(self, text: str, linebreaks=1, strip=False, significant_whitespaces=False,
                         ignore_minified=False):
        if not ignore_minified:
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
