from poc.classes.AuxST import AuxSTBlock
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateInstance(AuxSTBlock):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.property, i)
        self.def_type = AuxSymbolTable.predicateDeclaration
        self.id = ""
        self.zfrom = i.corrected_position('PredicateHeader')
        self.zto = i.last_positions_by_rule['PredicateInstance'].pos_to_str()
        self.keyword = ""
        self.mandatory = False



