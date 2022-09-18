from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTExtension(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.block_axiom, i)
        self.extension = ""

