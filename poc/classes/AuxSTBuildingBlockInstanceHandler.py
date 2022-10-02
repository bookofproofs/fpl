from poc.classes.AuxSTBuildingBlockInstanceVariable import AuxSTBuildingBlockInstanceVariable

"""
The class AuxSTBuildingBlockInstanceHandler provides methods for for storing and retrieving the state
of an evaluated instance of an FPL Building Block, while keeping the context of the evaluation.
"""


class AuxSTBuildingBlockInstanceHandler:
    def __init__(self, identifier):
        self.id = identifier
        self._vars = dict()
        self._ids = dict()
        self._registers = dict()

    def set_register(self, register):
        long_id = register.node.get_long_id()
        self._registers[long_id] = register

    def get_register(self, register_id):
        return self._registers[register_id]

    def has_register(self, register_id):
        return register_id in self._registers

    def add_instance_variable(self, var_id: str, occurrences: list, type_node):
        self._vars[var_id] = AuxSTBuildingBlockInstanceVariable(occurrences, type_node)

    def get_instance_variable(self, var_id):
        return self._vars[var_id]

    def add_identifier_with_expression(self, identifier, expression):
        if identifier in self._ids:
            AssertionError(identifier + " already registered with " + str(self._ids[identifier]))
        else:
            self._ids[identifier] = expression

    def get_identifiers_expression(self, identifier):
        return self._ids[identifier]

    def get_vars(self):
        return self._vars

    def clear_instance(self):
        for var_id in self._vars:
            self._vars[var_id].occurrences.clear()
        self._ids.clear()
        self._vars.clear()
        self._registers.clear()
