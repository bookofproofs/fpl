from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTStatementCaseSome(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_case, i)
        self.zfrom = i.corrected_position('Predicate')
        self.zto = i.last_positions_by_rule['ConditionFollowedByResult'].pos_to_str()
        # the default case statement's type is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementCaseSome(self._i)

    def evaluate(self, sem):
        raise NotImplementedError()