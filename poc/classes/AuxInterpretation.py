from classes.AuxAstInfo import AuxAstInfo

"""
The class Interpretation is the base class of all semantical interpretations that are possible in FPL
"""


class AuxInterpretation:
    # internal semantical representation of the rule
    _inter = None
    # any errors from the caller. Classes inheriting from AuxInterpretation can add to to this list own errors.
    _errors = None
    _ast_info = None

    def __init__(self, ast_info: AuxAstInfo, errors: list):
        self._ast_info = ast_info
        self._errors = errors

    def rule_name(self):
        """ name of the corresponding grammar rule """
        return self._ast_info.rule

    def rule_pos(self):
        """ Current parsing position of the parsed  file (in characters) """
        return self._ast_info.pos

    def rule_col(self):
        """ Current parsing column in the parsed file """
        return self._ast_info.col

    def rule_line(self):
        """ Current parsing line in the parsed file """
        return self._ast_info.line

    def rule_pos(self):
        return self._ast_info.pos

    def get_interpretation(self):
        return self._inter

    def set_interpretation(self, value):
        self._inter = value

    def clear_cst(self):
        """
        Once the interpretation has been determined, sets the field to None to save memory.
        """
        self._ast_info.cst = None

    def get_cst(self):
        """
        If the interpretation is not determined yet, the TatSu parsing context of the rule.
        Otherwise None.
        """
        return self._ast_info.cst

    def get_errors(self):
        return self._errors

    def get_ast_info(self):
        return self._ast_info

    def clone(self, other):
        self._ast_info = other.get_ast_info()
        self._errors = other.get_errors()

    def __str__(self):
        return self._ast_info.rule + ":" + str(self._ast_info.pos) + ":" + str(self._ast_info.col) + ":" + \
               str(self._ast_info.line) + ":" + str(self._inter).replace("\n", "\\n")
