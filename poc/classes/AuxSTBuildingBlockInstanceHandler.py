from poc.classes.AuxSTBuildingBlockInstanceVariable import AuxSTBuildingBlockInstanceVariable

"""
The class AuxSTBuildingBlockInstanceHandler provides methods for for storing and retrieving the state
of an evaluated instance of an FPL Building Block, while keeping the context of the evaluation.
"""


class AuxSTBuildingBlockInstanceHandler:
    def __init__(self, identifier):
        self.id = identifier
        self._my_vars = dict()
        self._my_ids = dict()

    def add_instance_variable(self, var_id: str, occurrences: list, type_node):
        self._my_vars[var_id] = AuxSTBuildingBlockInstanceVariable(occurrences, type_node)

    def get_instance_variable(self, var_id):
        return self._my_vars[var_id]

    def add_identifier_with_expression(self, identifier, expression):
        if identifier in self._my_ids:
            AssertionError(identifier + " already registered with " + str(self._my_ids[identifier]))
        else:
            self._my_ids[identifier] = expression

    def get_identifiers_expression(self, identifier):
        return self._my_ids[identifier]

    def get_vars(self):
        return self._my_vars

    def clear_instance(self):
        for var_id in self._my_vars:
            self._my_vars[var_id].occurrences.clear()
        self._my_ids.clear()
        self._my_vars.clear()
