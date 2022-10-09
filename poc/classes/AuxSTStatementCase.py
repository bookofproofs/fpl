from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxSTTypeInterface import AuxSTTypeInterface


class AuxSTStatementCase(AuxSTStatement, AuxSTTypeInterface):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_cases, i)
        self.zfrom = i.corrected_position('case')
        self.zto = i.last_positions_by_rule['CaseStatement'].pos_to_str()
        # the case statement's type is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementCase(self._i)

    def evaluate(self, sem):
        for child in self.children:
            if isinstance(child, AuxSTTypeInterface):
                # call evaluation differently for all children that have predefined types
                EvaluateParams.evaluate_recursion(sem, child, expected_type=child.get_declared_type())
            else:
                EvaluateParams.evaluate_recursion(sem, child)
        pass
