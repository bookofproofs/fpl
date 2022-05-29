from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTVarSpecList(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSymbolTable.var_spec)

    def clone(self):
        return AuxSTVarSpecList()
