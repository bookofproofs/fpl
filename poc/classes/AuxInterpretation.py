"""
The class Interpretation is the base class of all semantical interpretations that are possible in FPL
"""


class AuxInterpretation:
    # name of the corresponding grammar rule
    _rule = None
    # If the interpretation is not determined yet, the TatSu parsing context of the rule.
    # Otherwise (the interpretation has been determined, the field will be set to None to save memory.
    _cst = None
    # Current parsing position of the parsed  file (in characters)
    _pos = 0
    # Current parsing column in the parsed file
    _col = 0
    # Current parsing line in the parsed file
    _line = 0
    # internal semantical representation of the rule
    _inter = None
    # any errors from the caller. Classes inheriting from AuxInterpretation can add to to this list own errors.
    _errors = None

    def __init__(self, rule: str, pos: int, col: int, line: int, cst, errors: list):
        self._rule = rule
        self._col = col
        self._pos = pos
        self._line = line
        self._cst = cst
        self._errors = errors

    def rule_name(self):
        return self._rule

    def rule_pos(self):
        return self._pos

    def rule_col(self):
        return self._col

    def rule_line(self):
        return self._line

    def rule_pos(self):
        return self._pos

    def get_interpretation(self):
        return self._inter

    def set_interpretation(self, value):
        self._inter = value

    def clear_cst(self):
        self._cst = None

    def get_cst(self):
        return self._cst

    def get_errors(self):
        return self._errors

    def clone(self, other):
        self._rule = other.rule_name()
        self._col = other.rule_col()
        self._pos = other.rule_pos()
        self._line = other.rule_line()
        self._cst = other.get_cst()
        self._errors = other.get_errors()

    def __str__(self):
        return self._rule + ":" + str(self._pos) + ":" + str(self._col) + ":" + str(self._line) + ":" + \
               str(self._inter).replace("\n", "\\n")
