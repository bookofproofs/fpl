from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTCoords(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.coordinates, i)

    def clone(self):
        other = AuxSTCoords(self._i)
        other.zto = self.zto
        other.zfrom = self.zfrom
        for child in self.children:
            child_clone = child.clone()
            child_clone.parent = other
        return other
