from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTProofStop(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSTConstants.proofArgument)
        self.type = ""


