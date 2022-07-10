from poc.classes.AuxSTTheoremLikeStatementOrConjecture import AuxSTTheoremLikeStatementOrConjecture
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTCorollary(AuxSTTheoremLikeStatementOrConjecture):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_cor, i, i.corrected_position('CorollaryHeader'),
                         i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str())
