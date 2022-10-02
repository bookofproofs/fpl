from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTCoords(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.coordinates, i)

    def clone(self):
        return self._copy(AuxSTCoords(self._i))

    def to_string(self):
        ret = "coords["
        for child in self.children:
            ret += child.to_string()
        ret += "]"
        return ret

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.to_string()
        return self._long_id
