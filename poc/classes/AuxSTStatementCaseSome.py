from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTStatementCaseSome(AuxSTStatement):

    def __init__(self, i):
        super().__init__(AuxSTConstants.case, i)
        self.zfrom = i.corrected_position('Predicate')
        self.zto = i.last_positions_by_rule['ConditionFollowedByResult'].pos_to_str()
        # the case statement is a undefined
        self.set_declared_type(InbuiltUndefined(self))

    def clone(self):
        return AuxSTStatementCaseSome(self._i)

