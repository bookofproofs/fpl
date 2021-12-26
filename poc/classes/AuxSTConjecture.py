from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTConjecture(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_conj, i)
        self.zfrom = i.corrected_position('TheoremLikeStatementOrConjectureHeader')
        self.zto = i.last_positions_by_rule['TheoremLikeStatementOrConjecture'].pos_to_str()
