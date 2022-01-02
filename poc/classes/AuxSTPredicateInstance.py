from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTPredicateInstance(AuxSTInstance):

    def __init__(self, i):
        super().__init__(i)
        self.def_type = AuxSymbolTable.predicateInstance
        self.id = ""
        self.zfrom = i.corrected_position('PredicateHeader')
        self.zto = i.last_positions_by_rule['PredicateInstance'].pos_to_str()
        self.keyword = ""

