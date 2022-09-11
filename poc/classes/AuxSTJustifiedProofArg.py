from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxSTProofArgument import AuxSTProofArgument


class AuxSTJustifiedProofArg(AuxSTProofArgument):

    def __init__(self, i):
        super().__init__(i)

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltUndefined(self)
