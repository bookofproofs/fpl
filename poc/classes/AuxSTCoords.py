from poc.classes.AuxST import AuxST
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTCoords(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.coordinates, i)

    def clone(self):
        return self._copy(AuxSTCoords(self._i))
