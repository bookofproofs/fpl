from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTSelf(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSymbolTable.selfInstance)
        self.reference = None
        self.number_ats = 0
        self.id = AuxSymbolTable.selfInstance


