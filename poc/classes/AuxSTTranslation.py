from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTTranslation(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.translation, parsing_info)
        self.lang = ""
