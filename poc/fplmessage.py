import re


class FplParserError(Exception):

    def __init__(self, inner_exception, error_context):
        self.error_context = error_context
        result = re.search("\((\d+):(\d+)\)([^:]+)", self.error_context)
        # inner_exception = str(inner_exception).replace("\n", " ")
        if len(result.groups()) >= 2:
            self.__line = result.group(1)
            self.__col = result.group(2)
            self.__msg = str(inner_exception)
        else:
            self.__line = 0
            self.__col = 0
            self.__msg = ""

        self.inner_exception = inner_exception
        self.__type = str(type(self).__name__)
        self.mainType = "E"

    def __str__(self):
        msg = self.__type + " "
        pos = str(self.error_context).find("\n")
        if pos > -1:
            msg += self.error_context[:pos]

            msg += " " + str(self.inner_exception.stack)
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

    def __init__(self, msg: str, line: int, col: int, file: str):
        self.__msg = msg
        self.__line = line
        self.__col = col
        self.__type = str(type(self).__name__)
        self.mainType = "E"  # Error per default
        self.file = file

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
