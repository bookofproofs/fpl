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
        other = AuxSTQualified(self._i)
        other.zto = self.zto
        other.zfrom = self.zfrom
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = other
        return other
