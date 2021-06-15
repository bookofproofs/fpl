class FPLCompilerError(BaseException):

    def __init__(self, error_code, inner_exception, line_no, error_context):
        self.error_code = error_code
        self.error_context = error_context
        self.inner_exception = inner_exception
        self.line_no = line_no + 1

    def __str__(self):
        msg = ""
        if self.error_code != 0:
            msg += "no. " + str(self.error_code) + " (line " + str(self.line_no) + ") "

        if self.error_code >= 1000:
            msg += str(self.error_context)
        else:
            if self.error_code < -1:
                msg += "Unexpected error: " + str(type(self.inner_exception)) + " " + str(self.error_context)
            elif self.error_code == -1:
                msg += "Fpl Parse error: " + str(type(self.inner_exception)) + " " + str(self.error_context)
            elif self.error_code == 0:
                msg += "Syntax error "
                pos = str(self.error_context).find("\n")
                if pos > -1:
                    msg += self.error_context[:pos]
                    msg += str(self.inner_exception)
            elif self.error_code == 1:
                msg += "There is already an IDENTIFIER with the same name '" + str(self.error_context[2]) + "'"
                msg += " found at " + str(self.error_context[3]) + ":" + str(self.error_context[4]) + "."
            elif self.error_code == 2:
                msg += "The identifier '" + str(self.error_context[2]) + "' has to be PascalCase."
            elif self.error_code == 3:
                msg += "The variable '" + str(self.error_context[2]) + "' is not declared in the statement "
                msg += str(self.error_context[3]) + "."
            elif self.error_code == 4:
                msg += "deprecated: The IN qualifier is not allowed in the signature of the DEFINITION " + str(
                    self.error_context[2]) + "."
            elif self.error_code == 5:
                msg += "The theory has no declaration for '" + str(self.error_context[2]) + "'."
            elif self.error_code == 6:
                msg += "Multiple declarations for a variable not supported, the variable was '" + str(
                    self.error_context[2]) + "'."

        return msg
