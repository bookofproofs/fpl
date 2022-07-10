from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSymbolTable import AuxSymbolTable


class AuxSTProperties(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSymbolTable.properties)

    def evaluate(self, sem):
        for child in self.children:
            EvaluateParams.evaluate_recursion(sem, child, InbuiltUndefined())
        sem.eval_stack[-1].value = InbuiltUndefined()
