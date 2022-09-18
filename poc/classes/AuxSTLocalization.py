from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTLocalization(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.localization, i)
