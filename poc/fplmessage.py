import re


class FplInterpreterMessage(Exception):

    def __init__(self, msg: str, line: int, col: int, file: str):
        self._msg = msg
        self._line = line
        self._col = col
        self._type = str(type(self).__name__)
        self.mainType = "E"  # Error per default
        self.diagnose_id = "unknown"
        self.file = file

    def __str__(self):
        return self._type + ":" + str(self._line) + ":" + str(self._col) + ": " + self._msg

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return str(other) == self.__str__()

    def get_line(self):
        return self._line

    def get_col(self):
        return self._col

    def get_type(self):
        return self._type

    def get_msg(self):
        return self._msg

    def get_tkinter_pos(self):
        return str(self._line) + "." + str(int(self._col))

    def to_tuple(self):
        return self.diagnose_id, self._msg, self._line, self._col, self.file

    def sort_key(self):
        if self.diagnose_id.startswith("SY"):
            sort_diagnose_id = "A"
        else:
            sort_diagnose_id = "B"
        return self.mainType + sort_diagnose_id + self.file + str(self._line).zfill(6) + str(self._col).zfill(6)


class FplParserError(FplInterpreterMessage):

    def __init__(self, inner_exception, error_context, diagnose_id, file_name):
        super().__init__("", 0, 0, file_name)
        self.error_context = error_context
        if diagnose_id == 1:
            self.diagnose_id = "SY0010"  # Syntax parse error
            self._msg = "Syntax error, trying to parse"
        elif diagnose_id == 2:
            self.diagnose_id = "SY0020"  # Syntax token error
            self._msg = "Syntax error (token):"
        elif diagnose_id == 3:
            self.diagnose_id = "SY0030"  # Syntax pattern error
            self._msg = "Syntax error (pattern):"
        else:
            self.diagnose_id = "unknown"  # Unknown syntax Tatsu error
        result = re.search(r"\((\d+):(\d+)\)([^:]+)", self.error_context)
        if result is None:
            # other errors
            self._line = 1
            self._col = 0
            self._extract_parser_message(inner_exception)
        else:
            if len(result.groups()) >= 2:
                self._line = result.group(1)
                self._col = result.group(2)
                self._extract_parser_message(inner_exception)
            else:
                self._line = 1
                self._col = 0
                self._msg = ""

        self.inner_exception = inner_exception
        self._type = str(type(self).__name__)

    def _extract_parser_message(self, inner_exception):
        msg = str(inner_exception).split("\n")
        for chunk in reversed(msg):
            if "^" in chunk:
                break
            elif chunk not in ["CW"]:
                self._msg += " >" + chunk

    def __str__(self):
        msg = self._type + " "
        pos = str(self.error_context).find("\n")
        if pos > -1:
            msg += self.error_context[:pos]

            msg += " " + str(self.inner_exception.stack)
        return msg


class FplInterpreterSystemError(FplInterpreterMessage):
    def __init__(self, trace_back):
        super().__init__(trace_back, 0, 0, "")
