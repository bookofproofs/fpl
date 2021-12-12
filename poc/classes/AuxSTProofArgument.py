from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTProofArgument(AuxST):

    def __init__(self, parsing_info):
        super().__init__(AuxSymbolTable.proofArgument, parsing_info)
        self.type = ""
