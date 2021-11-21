"""
The class AuxContext provides methods to store and check the context during the parsing process helping to identify
in which context a grammar rule was used.
"""


class AuxContext:
    aftercase = "aftercase"
    axiom = "axiom"
    bound = "bound"
    block = "block"
    case = "case"
    classConstructor = "constructor"
    classDeclaration = "class"
    classInstanceDeclaration = "classInstanceDeclaration"
    classType = "classtype"
    dolinebreaks = "dolinereaks"
    functionalTerm = "functionalTerm"
    functionalTermImage = "image"
    inferenceRule = "inferenceRule"
    inferenceRules = "inferenceRules"
    insideproof = "insideproof"
    isoperator = "isoperator"
    mandatoryProperty = "mandatoryProperty"
    nolinebreak = "nolinebreak"
    optionalProperty = "optionalProperty"
    paren = "paren"
    predicateDeclaration = "predicate"
    root = "root"
    signature = "signature"
    theoremLikeStmtConj = "conjecture"
    theoremLikeStmtCor = "corollary"
    theoremLikeStmtLem = "lemma"
    theoremLikeStmtProp = "proposition"
    theoremLikeStmtThm = "theorem"
    theory = "theory"
    uses = "uses"
    varDeclaration = "varDeclaration"

    def __init__(self):
        """
        Constructor of Context
        """
        # used to distinguish different contexts while parsing and interpreting the same lexemes
        self._context_stack = []

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

    def push_context(self, key, debug=None):
        """
        Pushes the parsing context on a stack
        :param key: key of the context
        :param debug: if not none, the current stack will be printed with this debug information
        :return: None
        """
        self._context_stack.append(key)
        if debug is not None:
            print(str(self._context_stack), str(debug), "push " + key)

    def pop_context(self, pars: list, debug=None):
        """
        Pops the last context from the stack.
        :param pars: a context (list) assumed to be at the tail of the stack. Raises an AssertionError if not
        :param debug: if not none, the current stack will be printed with this debug information
        :return: None
        """
        if type(pars) is list:
            if len(self._context_stack) >= len(pars):
                if not self.is_parsing_context(pars):
                    raise AssertionError(
                        "Got context " + str(self._context_stack[-len(pars):]) + ", expected " + str(list(pars)))
                else:
                    self._context_stack = self._context_stack[:len(self._context_stack) - len(pars)]
            else:
                raise AssertionError("Got context " + str(self._context_stack) + ", expected " + str(pars))
        else:
            raise TypeError("Got context " + str(type(pars)) + ", expected " + str(type(list)))
        if debug is not None:
            print(self._context_stack, debug, "pop " + str(pars))

    def get_context(self):
        return self._context_stack
