from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTTranslation(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.translation, i)
        self.lang = ""
