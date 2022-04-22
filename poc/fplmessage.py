import re


class FplInterpreterMessage(Exception):

    def __init__(self, msg: str, line: int, col: int, file: str):
        self.__msg = msg
        self.__line = line
        self.__col = col
        self.__type = str(type(self).__name__)
        self.mainType = "E"  # Error per default
        self.diagnose_id = "unknown"
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

    def get_tkinter_pos(self):
        return str(self.__line) + "." + str(int(self.__col) - 1)

    def to_tuple(self):
        return self.diagnose_id, self.__msg, self.__line, self.__col


class FplParserError(FplInterpreterMessage):

    def __init__(self, inner_exception, error_context, diagnose_id, file_name):
        super().__init__("", 0, 0, file_name)
        self.error_context = error_context
        if diagnose_id == 1:
            self.diagnose_id = "SY0010"  # Syntax parse error
        elif diagnose_id == 2:
            self.diagnose_id = "SY0020"  # Syntax token error
        elif diagnose_id == 3:
            self.diagnose_id = "SY0030"  # Syntax pattern error
        else:
            self.diagnose_id = "unknown"  # Unknown syntax Tatsu error
        result = re.search("\((\d+):(\d+)\)([^:]+)", self.error_context)
        if result is None:
            # other errors
            self.__line = 1
            self.__col = 0
            self.__msg = str(inner_exception)
        else:
            if len(result.groups()) >= 2:
                self.__line = result.group(1)
                self.__col = result.group(2)
                self.__msg = str(inner_exception)
            else:
                self.__line = 1
                self.__col = 0
                self.__msg = ""

        self.inner_exception = inner_exception
        self.__type = str(type(self).__name__)

    def __str__(self):
        msg = self.__type + " "
        pos = str(self.error_context).find("\n")
        if pos > -1:
            msg += self.error_context[:pos]

            msg += " " + str(self.inner_exception.stack)
        return msg
