from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTLocalization(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.localization, parsing_info)
