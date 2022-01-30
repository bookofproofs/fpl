from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTRange(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.rng, i)
        self.left_included = False
        self.right_included = False

    def to_string(self):
        ret = "range["
        if not self.left_included:
            ret += "!"
            for child in self.children:
                ret += child.to_string()
        if not self.right_included:
            ret += "!"
        ret += "]"
        return ret

    def clone(self):
        other = AuxSTRange(self._i)
        other.zto = self.zto
        other.zfrom = self.zfrom
        other.left_included = self.left_included
        other.right_included = self.right_included
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = other
        return other
