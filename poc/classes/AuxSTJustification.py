from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTJustification(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.justification, i)

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltUndefined(self)
