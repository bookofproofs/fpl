from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTCoords(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.coordinates, i)

    def clone(self):
        return self._copy(AuxSTCoords(self._i))
