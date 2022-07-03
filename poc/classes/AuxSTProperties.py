from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTProperties(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSymbolTable.properties)

    def evaluate(self, sem):
        # todo: implement
        pass
