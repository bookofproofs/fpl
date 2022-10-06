from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement


class AuxSTStatementRange(AuxSTStatement):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_range, i)
        self.zfrom = i.corrected_position('range')
        self.zto = i.last_positions_by_rule['RangeStatement'].pos_to_str()

    def clone(self):
        return AuxSTStatementRange(self._i)

    def evaluate(self, sem):
        raise NotImplementedError()