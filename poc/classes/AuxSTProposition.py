from poc.classes.AuxSTTheoremLikeStatementOrConjecture import AuxSTTheoremLikeStatementOrConjecture
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTProposition(AuxSTTheoremLikeStatementOrConjecture):

    def __init__(self, i):
        super().__init__(AuxSTConstants.block_prop, i, i.corrected_position('TheoremLikeStatementOrConjectureHeader'),
                         i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str())
