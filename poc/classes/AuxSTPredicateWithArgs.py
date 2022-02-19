from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateWithArgs(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.predicate_with_arguments, i)
        self.reference = None

    def clone(self):
        new_predicate = self._copy(AuxSTPredicateWithArgs(self._i))
        new_predicate.id = self.id
        new_predicate.outline = self.outline
        return new_predicate

