from poc.classes.AuxST import AuxST
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInbuiltTypes import InbuiltUndefined


class AuxSTJustification(AuxST):

    def __init__(self, i):
        super().__init__(AuxSymbolTable.justification, i)

    def evaluate(self, sem):
        sem.eval_stack[-1].value = InbuiltUndefined()