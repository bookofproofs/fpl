from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTLocalizations(AuxSTOutline):

    def __init__(self, parent: AuxSTOutline):
        super().__init__(parent, AuxSTConstants.localization_root)
