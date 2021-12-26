from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTAxiom(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.block_axiom, i)
        self.zfrom = i.corrected_position('AxiomHeader')
        self.zto = i.last_positions_by_rule['Axiom'].pos_to_str()
        self.keyword = ""


