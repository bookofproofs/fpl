from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTProofArgument(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.proofArgument, i)
        self.type = ""

    def evaluate(self, sem):
        raise NotImplementedError()
