from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTProperties(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSTConstants.properties)

    def evaluate(self, sem):
        for child in self.children:
            expected_type = child.get_declared_type()
            EvaluateParams.evaluate_recursion(sem, child, expected_type=expected_type)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = "AuxSTProperties"
        return self._long_id
