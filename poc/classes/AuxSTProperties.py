from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTProperties(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSTConstants.properties)
        # the properties node in the symbol table has the inbuilt undefined type per default
        self.set_declared_type(InbuiltUndefined(self.parent))

    def evaluate(self, sem):
        for child in self.children:
            expected_type = child.get_declared_type()
            EvaluateParams.evaluate_recursion(sem, child, expected_type)
        sem.eval_stack[-1].value = InbuiltUndefined(self.parent)
