from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTExtension(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_axiom, i)
        self.extension = ""
