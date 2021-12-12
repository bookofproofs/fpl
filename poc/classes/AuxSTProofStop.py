from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTProofStop(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSymbolTable.proofArgument)
        self.type = ""


