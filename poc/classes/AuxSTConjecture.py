from poc.classes.AuxSTTheoremLikeStatementOrConjecture import AuxSTTheoremLikeStatementOrConjecture
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTConjecture(AuxSTTheoremLikeStatementOrConjecture):
    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_conj, i, i.corrected_position('TheoremLikeStatementOrConjectureHeader'),
                         i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str())
