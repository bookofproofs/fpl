from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxSTVarDec import AuxSTVarDec
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTVarSpecList(AuxSTOutline):

    def __init__(self):
        super().__init__(None, AuxSTConstants.var_spec)
        # var spec lists have the inbuilt undefined type per default
        self.set_declared_type(InbuiltUndefined(self.parent))

    def clone(self):  # noqa
        return AuxSTVarSpecList()

    def evaluate(self, sem):
        for child in self.children:
            if isinstance(child, AuxSTVarDec):
                # initialize the declared type of AuxSTVarDec nodes
                child.set_declared_type(InbuiltUndefined(child))
            expected_type = self._determine_exptected_type(child)
            EvaluateParams.evaluate_recursion(sem, child, expected_type)
        sem.eval_stack[-1].value = InbuiltUndefined(self.parent)

    def _determine_exptected_type(self, child):
        return InbuiltUndefined(child)
