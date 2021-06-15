from classes.Variable import Variable


class FPLSemantics(object):
    errors = None
    warnings = None
    parse_list = None
    _stack = None
    _minified = None
    _last_cst = None
    _context_stack = None  # used to distinguish different contexts while parsing and interpreting the same lexemes

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.parse_list = []
        self._stack = []
        self._minified = ""
        self._last_cst = ""
        self._context_stack = []  # used to distinguish different contexts while parsing and interpreting the same lexemes

    def get_minified(self):
        return self._minified

    @staticmethod
    def _debug():
        return True

    def _default(self, ast):
        self.last_ast = ast
        return ast

    def _minify(self, context):
        """
        Builds up a minified representation of the parsed fpl file during the parsing process
        :param context: parsing context
        :return:
        """
        rule = context.rule[0]
        if self._minified.find("ret Succ(Succ(Zero()))else") > -1:
            print("")
            pass
        if isinstance(context.cst, str):
            if rule == "Comment":
                pass
            elif rule == "LongComment":
                pass
            elif rule == "IW":
                pass
            elif rule == "CW":
                pass
            elif rule == "SW":
                self._minified += " "
            elif rule == "RightParen":
                self._minified += ")"
            elif rule == "RightBrace":
                self._minified += "}"
            elif rule == "RightChevron":
                self._minified += ">"
            elif rule == "tpl" and self._last_cst[0:3] == context.cst:
                self._last_cst = context.cst
            elif rule == "ret" and self._last_cst[0:3] == context.cst:
                self._last_cst = context.cst
            else:
                if self._last_cst == context.cst:
                    # prevent repeating of the parsed text because of nested productions
                    pass
                else:
                    self._last_cst = context.cst
                    # replace long versions by short versions
                    if context.cst == "assume":
                        self._minified += "ass"
                    elif context.cst == "axiom":
                        self._minified += "ax"
                    elif context.cst == "class":
                        self._minified += "cl"
                    elif context.cst == "conclusion":
                        self._minified += "con"
                    elif context.cst == "conjecture":
                        self._minified += "conj"
                    elif context.cst == "corollary":
                        self._minified += "cor"
                    elif context.cst == "function":
                        self._minified += "func"
                    elif context.cst == "inference":
                        self._minified += "inf"
                    elif context.cst == "lemma":
                        self._minified += "lem"
                    elif context.cst == "mandatory":
                        self._minified += "mand"
                    elif context.cst == "premise":
                        self._minified += "pre"
                    elif context.cst == "object":
                        self._minified += "obj"
                    elif context.cst == "optional":
                        self._minified += "opt"
                    elif context.cst == "predicate":
                        self._minified += "pred"
                    elif context.cst == "premise":
                        self._minified += "pre"
                    elif context.cst == "postulate":
                        self._minified += "post"
                    elif context.cst == "proof":
                        self._minified += "prf"
                    elif context.cst == "proposition":
                        self._minified += "prop"
                    elif context.cst == "return":
                        self._minified += "ret"
                    elif context.cst == "revoke":
                        self._minified += "ref"
                    elif context.cst == "syntax":
                        self._minified += "syn"
                    elif context.cst == "template":
                        self._minified += "tpl"
                    elif context.cst == "theorem":
                        self._minified += "thm"
                    elif context.cst == "theory":
                        self._minified += "th"
                    elif context.cst == "undefined":
                        self._minified += "undef"
                    else:
                        self._minified += context.cst

    def _postproc(self, context, ast):
        # minify
        self._minify(context)
        d = dict()
        d["rule"] = context.rule[0]
        d["cst"] = context.cst
        d["pos"] = context.pos
        d["col"] = context.tokenizer.col
        d["line"] = context.tokenizer.line
        self.interpret(d, context)
        self.parse_list.append(d)
        return ast

    def interpret(self, d, context):
        inter = None
        rule = d["rule"]
        if rule == "IdStartsWithSmallCase":
            inter = context.cst
        elif rule == "Decimal":
            inter = context.cst
        elif context.cst == "definition" or context.cst == "def":
            inter = context.cst
        elif rule == "DefinitionHeader":
            inter = self._stack.pop()  # copy of "definition" or "def"
            self._context_stack.append("def")  # mark the beginning of a Definition
        elif rule == "NumberOrCamelCaseId":
            inter = self._stack.pop()  # copy of "CamelCaseId" or "Decimal"
        elif rule == "IdStartsWithCap":
            inter = context.cst
        elif rule == "obj":
            inter = context.cst
        elif rule == "object":
            inter = context.cst
        elif rule == "ObjectHeader":
            inter = self._stack.pop()  # copy of "object" or "obj" or "template" or "tpl"
            if self.is_parsing_context("def") and (inter == "object" or inter == "obj"):
                self._context_stack.append("obj")  # mark the beginning of DefinitionObject
            elif self.is_parsing_context("def") and (inter == "template" or inter == "tpl"):
                self._context_stack.append("tpl")  # mark the beginning of DefinitionObject using a generic type
        elif rule == "ObjectType":
            inter = self._stack.pop()  # copy of "PascalCaseId"
        elif rule == "ObjVariableType":
            inter = self._stack.pop()  # copy of ObjectHeader or ObjectType
            if self.is_parsing_context("def", "obj", "PredicateIdentifier") \
                    or self.is_parsing_context("def", "tpl", "PredicateIdentifier"):
                self._context_stack.append("ObjVariableType")  # continue the beginning of DefinitionObject
                # at this stage, we know that
        elif rule == "IdStartsWithCap":
            inter = context.cst
        elif rule == "PredicateIdentifier":
            inter = self._stack.pop()  # copy of "PascalCaseId"
            if self.is_parsing_context("def", "obj") or self.is_parsing_context("def", "tpl"):
                self._context_stack.append("PredicateIdentifier")  # continue the beginning of DefinitionObject
        elif rule == "tpl":
            inter = context.cst
        elif rule == "template":
            inter = context.cst
        elif rule == "Variable":
            inter = Variable(self._stack.pop())
        d['inter'] = inter
        self._stack.append(inter)

    def is_parsing_context(self, *pars):
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
                is_context = is_context and (x == self._context_stack[pos]['key'])
                if not is_context:
                    break
                pos += 1
            return is_context

    def push_context(self, key, value):
        """
        Pushes the context on a stack
        :param key: key of the context
        :param value: value of the context
        :return: None
        """
        d = dict()
        d['key'] = key
        d['val'] = value
        self._context_stack.append(d)

    def pop_context(self):
        """
        pops the last context from the stack
        :return: a dict with d['key'] == <key>, d['val'] == <val>
        """
        if len(self._context_stack) > 0:
            return self._context_stack.pop()
        else:
            return None
