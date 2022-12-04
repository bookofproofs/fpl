from poc.classes.AuxST import AuxST
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxSTProofStop import AuxSTProofStop
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxSTConstants import AuxSTConstants


class AuxSTProofArgument(AuxST):

    def __init__(self, i):
        super().__init__(AuxSTConstants.proofArgument, i)

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = ""
            for arg in self.children:
                self._long_id += arg.get_long_id()
        return self._long_id

    def evaluate(self, sem):
        new_value = InbuiltValuePredicate(self)
        sem.eval_stack[-1].value = new_value
        for child in self.children:
            if isinstance(child, AuxSTProofStop):
                ret = EvaluateParams.evaluate_recursion(sem, child, expected_type=InbuiltPredicate(child))
                if ret.evaluation_error:
                    new_value.set_undetermined()
                else:
                    new_value.set_true()
                    new_value.set_expression(True)
            else:
                raise NotImplementedError(str(type(child)))
