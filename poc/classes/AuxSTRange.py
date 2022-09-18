from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTRange(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.rng, i)
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
        other = self._copy(AuxSTRange(self._i))
        other.left_included = self.left_included
        other.right_included = self.right_included
        return other
