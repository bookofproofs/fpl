from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTExtension(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.block_axiom, parsing_info)
        self.extension = ""

