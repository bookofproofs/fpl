from poc.classes.AuxST import AuxST


class AuxSTVarDec(AuxST):

    def __init__(self, i):
        super().__init__("var_decl", i)
        self._scope_start_row = 0
        self._scope_start_col = 0
        self._scope_end_row = 0
        self._scope_end_col = 0

    def clone(self):
        other = self._copy(AuxSTVarDec(self._i))
        other.id = self.id
        return other

    def initialize_scope(self, zto:str):
        """
        Initializes the scope of this variable declaration.
        By default, the scope starts with the beginning of the variable declaration and ends with the scope of the
        block, in which this declaration is found within the FPL code.
        :param zto: End of the scope when initializing the variable declaration.
        :return: None
        """
        sp = self.zfrom.split(".")
        self._scope_start_row = int(sp[0])
        self._scope_start_col = int(sp[1])
        sp = zto.split(".")
        self._scope_end_row = int(sp[0])
        self._scope_end_col = int(sp[1])

    def has_in_scope(self, pos: str):
        """
        Checks if a position (usually of a variable) is in the scope of the variable (self)
        :param zfrom: position
        :return: True if yes, False if no
        """
        sp = pos.split(".")
        row = int(sp[0])
        col = int(sp[1])
        if row < self._scope_start_row:
            return False
        if row == self._scope_start_row and col < self._scope_start_col:
            return False
        if row > self._scope_end_row:
            return False
        if row == self._scope_start_row and col < self._scope_start_col:
            return False
        return True
