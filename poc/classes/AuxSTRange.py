from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTRange(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.rng, parsing_info)
        self.left_included = False
        self.right_included = False
