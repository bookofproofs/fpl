from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTConstructor(AuxSTBlock):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.classConstructor, parsing_info)
        self.id = ""

