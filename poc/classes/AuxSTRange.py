from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTRange(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.rng, i)
        self.left_included = False
        self.right_included = False
