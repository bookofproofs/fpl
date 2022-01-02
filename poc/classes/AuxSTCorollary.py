from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTCorollary(AuxSTBlockWithSignature):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_cor, i)
        self.zfrom = i.corrected_position('CorollaryHeader')
        self.zto = i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str()
