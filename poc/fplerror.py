from classes.AuxInterpretation import AuxInterpretation
import re


class FplParserError(Exception):
    __line = 0
    __col = 0
    __msg = ""
    __type = None
    mainType = None

    def __init__(self, inner_exception, error_context):
        self.error_context = error_context
        result = re.search("\((\d+):(\d+)\)([^:]+)", self.error_context)
        # inner_exception = str(inner_exception).replace("\n", " ")
        if len(result.groups()) >= 2:
            self.__line = result.group(1)
            self.__col = result.group(2)
            self.__msg = str(inner_exception)

        self.inner_exception = inner_exception
        self.__type = str(type(self).__name__)
        self.mainType = "E"

    def __str__(self):
        msg = self.__type
        pos = str(self.error_context).find("\n")
        if pos > -1:
            msg += self.error_context[:pos]
            msg += str(self.inner_exception)
        return msg

    def get_line(self):
        return self.__line

    def get_col(self):
        return self.__col

    def get_type(self):
        return self.__type

    def get_msg(self):
        return self.__msg

    def to_tuple(self):
        return str(type(self).__name__), self.__msg, self.__line, self.__col


class FplInterpreterMessage(Exception):
    __msg = None
    __line = None
    __col = None
    __type = None
    mainType = None

    def __init__(self, msg: str, line: int, col: int):
        self.__msg = msg
        self.__line = line
        self.__col = col
        self.__type = str(type(self).__name__)
        self.mainType = "E"  # Error per default

    def __str__(self):
        return self.__type + ":" + str(self.__line) + ":" + str(self.__col) + ": " + self.__msg

    def get_line(self):
        return self.__line

    def get_col(self):
        return self.__col

    def get_type(self):
        return self.__type

    def get_msg(self):
        return self.__msg

    def to_tuple(self):
        return self.__type, self.__msg, self.__line, self.__col


class FplVariableDuplicateInVariableList(FplInterpreterMessage):
    def __init__(self, inter: AuxInterpretation, var_name: str):
        FplInterpreterMessage.__init__(self, var_name + " was already listed",
                                       inter.rule_line(),
                                       inter.rule_col())
        self.mainType = "W"  # Warning


class FplUnclosedScope(FplInterpreterMessage):
    def __init__(self, inter: AuxInterpretation, expected: str):
        FplInterpreterMessage.__init__(self, "Expected " + str(expected) + ", got " + str(inter.get_interpretation()),
                                       inter.rule_line(),
                                       inter.rule_col())


class FplUnopenedScope(FplInterpreterMessage):
    def __init__(self, inter: AuxInterpretation):
        FplInterpreterMessage.__init__(self, str(inter.get_interpretation()),
                                       inter.rule_line(),
                                       inter.rule_col())


class FplIdentifierAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, inter: AuxInterpretation, existing_inter: AuxInterpretation):
        FplInterpreterMessage.__init__(self, "Identifier " + str(inter.get_interpretation()) +
                                       " already defined at (" +
                                       str(existing_inter.rule_line()) + "," + str(existing_inter.rule_col()) + ")",
                                       inter.rule_line(),
                                       inter.rule_col())


class FplNameSpaceAlreadyExists(FplInterpreterMessage):
    def __init__(self, inter: AuxInterpretation, existing_inter: AuxInterpretation):
        FplInterpreterMessage.__init__(self, "Namespace " + str(inter.get_interpretation()) +
                                       " already defined at (" +
                                       str(existing_inter.rule_line()) + "," + str(existing_inter.rule_col()) + ")",
                                       inter.rule_line(),
                                       inter.rule_col())
