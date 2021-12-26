from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTProofArgument(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.proofArgument, i)
        self.type = ""
