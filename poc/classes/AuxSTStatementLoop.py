from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTStatementLoop(AuxSTStatement):

    def __init__(self, i):
        super().__init__(AuxSTConstants.statement_loop, i)
        self.zfrom = i.corrected_position('loop')
        self.zto = i.last_positions_by_rule['LoopStatement'].pos_to_str()
        # the loop statement is a undefined
        self.set_declared_type(InbuiltUndefined(self))

    def clone(self):
        return AuxSTStatementLoop(self._i)
