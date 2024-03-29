from poc.classes.AuxEvaluationBlockPredicate import AuxEvaluationBlockPredicate
from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTPredicateInstance(AuxSTInstance):

    def __init__(self, i):
        super().__init__(i)
        self.def_type = AuxSTConstants.predicateInstance
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

    def evaluate(self, sem):
        AuxEvaluationBlockPredicate.evaluate(self, sem)

    def get_declared_type(self):
        if self._declared_type is None:
            AuxEvaluationBlockPredicate.initialize_declared_type_of_predicate(self)
        return self._declared_type
