from poc.classes.AuxSTTheoremLikeStatementOrConjecture import AuxSTTheoremLikeStatementOrConjecture
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTConjecture(AuxSTTheoremLikeStatementOrConjecture):
    def __init__(self, i):
        super().__init__(AuxSTConstants.block_conj, i, i.corrected_position('TheoremLikeStatementOrConjectureHeader'),
                         i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str())

    def evaluate(self, sem):
        super().evaluate(sem)
        sem.eval_stack[-1].value.set_undetermined()
