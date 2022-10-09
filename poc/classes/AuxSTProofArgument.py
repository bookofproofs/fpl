from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTProofArgument(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.proofArgument, i)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = ""
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def evaluate(self, sem):
        raise NotImplementedError()
