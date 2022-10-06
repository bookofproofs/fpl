from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement


class AuxSTStatementAssign(AuxSTStatement):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_assign, i)
        self.zfrom = i.corrected_position('Assignee')
        self.zto = i.last_positions_by_rule['AssignmentStatement'].pos_to_str()

    def clone(self):
        return AuxSTStatementAssign(self._i)

    def evaluate(self, sem):
        raise NotImplementedError()