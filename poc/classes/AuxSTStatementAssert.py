from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltPredicate


class AuxSTStatementAssert(AuxSTStatement):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_assert, i)
        self.zfrom = i.corrected_position('assert')
        self.zto = i.last_positions_by_rule['AssertionStatement'].pos_to_str()
        # the assert statement is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementAssert(self._i)

    def evaluate(self, sem):
        raise NotImplementedError()