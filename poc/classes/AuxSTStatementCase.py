from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxSTTypeInterface import AuxSTTypeInterface


class AuxSTStatementCase(AuxSTStatement, AuxSTTypeInterface):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_cases, i)
        self.zfrom = i.corrected_position('case')
        self.zto = i.last_positions_by_rule['CaseStatement'].pos_to_str()

    def clone(self):
        return AuxSTStatementCase(self._i)
