from classes.AuxInterpretation import AuxInterpretation


class FplParserException(Exception):

    def __init__(self, inner_exception, error_context):
        self.error_context = error_context
        self.inner_exception = inner_exception

    def __str__(self):
        msg = str(type(self))
        pos = str(self.error_context).find("\n")
        if pos > -1:
            msg += self.error_context[:pos]
            msg += str(self.inner_exception)
        return msg


class FplInterpreterException(Exception):
    __msg = None
    __line = None
    __col = None

    def __init__(self, msg: str, line: int, col: int):
        self.__msg = msg
        self.__line = line
        self.__col = col

    def __str__(self):
        return str(type(self).__name__) + ":" + str(self.__line) + ":" + str(self.__col) + ": " + self.__msg

    def get_line(self):
        return self.__line

    def get_col(self):
        return self.__col


class FplVariableDuplicateInVariableListException(FplInterpreterException):
    def __init__(self, inter: AuxInterpretation, var_name: str):
        FplInterpreterException.__init__(self, var_name + " was already listed",
                       inter.rule_line(),
                       inter.rule_col())


class FplUnclosedScopeException(FplInterpreterException):
    __inter = None
    __expected = None

    def __init__(self, inter: AuxInterpretation, expected: str):
        FplInterpreterException.__init__(self, "Expected " + str(expected) + ", got " + str(inter.get_interpretation()),
                       inter.rule_line(),
                       inter.rule_col())


class FplUnopenedScopeException(Exception):
    __inter = None

    def __init__(self, inter: AuxInterpretation):
        FplInterpreterException.__init__(self, str(inter.get_interpretation()),
                       inter.rule_line(),
                       inter.rule_col())
