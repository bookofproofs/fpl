from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTStatementReturn(AuxSTStatement):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_return, i)
        self.zfrom = i.corrected_position('ReturnHeader')
        self.zto = i.last_positions_by_rule['ReturnStatement'].pos_to_str()
        # the return statement is a undefined
        self.set_declared_type(InbuiltUndefined(self))

    def clone(self):
        return AuxSTStatementReturn(self._i)
