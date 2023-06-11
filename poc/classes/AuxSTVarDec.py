from poc.classes.AuxSTWithId import AuxSTWithId
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTVarDec(AuxSTWithId):

    def __init__(self, i):
        super().__init__(AuxSTConstants.var_decl, i)
        self._scope_start_row = 0
        self._scope_start_col = 0
        self._scope_end_row = 0
        self._scope_end_col = 0

    def clone(self):
        other = self._copy(AuxSTVarDec(self._i))
        other.id = self.id
        return other

    def initialize_scope(self, zto: str):
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
        :param pos: position
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

    def evaluate(self, sem):
        """
        In the evaluate method of the variable declaration, we set the
        value of all variable usages to the default constructors
        :param sem:
        :return: None
        """
        node_of_declaration = self.parent.parent
        main_instance = node_of_declaration.get_main_instance()
        var = main_instance.get_instance_variable(self.id)
        for occurrence in var.occurrences:
            # set the pointer to the type of each usage of the variable inside the node to the same type_node
            occurrence.set_declared_type(var.type_node)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = "AuxSTVarDec_" + self.id
        return self._long_id
