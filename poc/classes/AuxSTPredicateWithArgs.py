from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateWithArgs(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.predicate_with_arguments, i)
        self.reference = None

    def clone(self):
        return self._copy(AuxSTPredicateWithArgs(self._i))

