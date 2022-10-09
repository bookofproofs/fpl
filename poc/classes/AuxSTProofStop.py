from poc.classes.AuxEvaluationPredicate import AuxEvaluationPredicate
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTTypeInterface import AuxSTTypeInterface


class AuxSTProofStop(AuxSTOutline, AuxSTTypeInterface, AuxEvaluationPredicate):

    def __init__(self):
        super().__init__(None, AuxSTConstants.proofArgument)
        self.type = ""

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.type
        return self._long_id

    def evaluate(self, sem):
        new_value = InbuiltValuePredicate(self)
        new_value.set_true()
        new_value.set_expression(True)
        sem.eval_stack[-1].value = new_value
