from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTTheorem(AuxSTBlockWithSignature):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_thm, i)
        self.zfrom = i.corrected_position('TheoremLikeStatementOrConjectureHeader')
        self.zto = i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str()

    def evaluate(self, sem):
        raise NotImplementedError()
