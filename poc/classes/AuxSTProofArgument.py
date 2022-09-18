from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTProofArgument(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.proofArgument, i)
        self.type = ""

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltUndefined(self)
