from poc.classes.AuxSTTheoremLikeStatementOrConjecture import AuxSTTheoremLikeStatementOrConjecture
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTLemma(AuxSTTheoremLikeStatementOrConjecture):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_lem, i, i.corrected_position('TheoremLikeStatementOrConjectureHeader'),
                         i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str())
