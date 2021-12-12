from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTLocalizations(AuxSTOutline):

    def __init__(self, parent: AuxSTOutline):
        super().__init__(parent, AuxSymbolTable.localization_root)
