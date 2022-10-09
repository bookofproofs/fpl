from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxSTTypeInterface import AuxSTTypeInterface


class AuxSTStatementIsOp(AuxSTStatement, AuxSTTypeInterface):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_is, i)
        self.zfrom = i.corrected_position('is')
        self.zto = i.last_positions_by_rule['IsOperator'].pos_to_str()
        # the is operator's type is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementIsOp(self._i)

    def evaluate(self, sem):
        raise NotImplementedError()
