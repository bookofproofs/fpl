from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTQualified(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.qualified, i)

    def to_string(self):
        ret = "dot["
        for child in self.children:
            ret += child.to_string()
        ret += "]"
        return ret

    def clone(self):
        return self._copy(AuxSTQualified(self._i))
