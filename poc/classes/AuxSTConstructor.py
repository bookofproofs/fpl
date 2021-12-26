from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTConstructor(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.classConstructor, i)
        self.id = ""

