from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTStatementCaseDefault(AuxSTStatement, AuxInterfaceSTType):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_case_default, i)
        self.zfrom = i.corrected_position('else')
        self.zto = i.last_positions_by_rule['DefaultResult'].pos_to_str()
        # the some case statement's type is a predicate
        self.set_declared_type(InbuiltPredicate(self))

    def clone(self):
        return AuxSTStatementCaseDefault(self._i)

    def evaluate(self, sem):
        raise NotImplementedError()