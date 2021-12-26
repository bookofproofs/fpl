from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTProof(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_proof, i)
        self.zfrom = i.corrected_position('ProofHeader')
        self.zto = i.last_positions_by_rule['Proof'].pos_to_str()
