from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTVarSpecList(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSTConstants.var_spec)

    def clone(self):  # noqa
        return AuxSTVarSpecList()

    def evaluate(self, sem):
        for child in self.children:
            EvaluateParams.evaluate_recursion(sem, child)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = "AuxSTVarSpecList"
        return self._long_id
