from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTJustification(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.justification, i)

    def evaluate(self, sem):
        raise NotImplementedError()
