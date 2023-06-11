from anytree import AnyNode
from poc.classes.AuxEvaluationPredicate import AuxEvaluationPredicate
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTProofStop(AuxSTOutline, AuxInterfaceSTType, AuxEvaluationPredicate):

    def __init__(self):
        super().__init__(AnyNode(), AuxSTConstants.proofArgument)
        self.type = ""
        self.zfrom = ""
        self.zto = ""

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.type
        return self._long_id

    def evaluate(self, sem):
        new_value = InbuiltValuePredicate(self)
        new_value.set_true()
        new_value.set_expression(True)
        sem.eval_stack[-1].value = new_value
