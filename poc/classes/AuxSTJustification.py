from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTJustification(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.justification, parsing_info)
