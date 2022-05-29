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

    def clone(self):
        new_predicate = self._copy(AuxSTPredicateInstance(self._i))
        new_predicate.id = self.id
        new_predicate.def_type = self.def_type
        new_predicate.keyword = self.keyword
        new_predicate.zfrom = self.zfrom
        new_predicate.to = self.zto
        new_predicate.mandatory = self.mandatory
        new_predicate._is_inherited = True
        return new_predicate



