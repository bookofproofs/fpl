from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTEbnfString(AuxSTOutline):

    def __init__(self):
        super().__init__(parent=None, outline=AuxSymbolTable.ebnf_string)  # noqa
        self.string = ""
