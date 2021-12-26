from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTTranslation(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.translation, i)
        self.lang = ""
