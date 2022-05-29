from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateWithArgs(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.predicate_with_arguments, i)
        self.reference = None
        # In case, a variable is used as a predicate with arguments,
        # this field will contain a pointer to the type in the symbol table with which this variable was declared
        self._declared_type = None

    def clone(self):
        new_predicate = self._copy(AuxSTPredicateWithArgs(self._i))
        new_predicate.id = self.id
        new_predicate.outline = self.outline
        new_predicate._declared_type = self._declared_type
        return new_predicate

    def set_declared_type(self, node):
        self._declared_type = node

    def get_declared_type(self):
        return self._declared_type
