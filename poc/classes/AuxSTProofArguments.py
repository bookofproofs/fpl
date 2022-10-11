import z3
from poc.classes.AuxEvaluationPredicate import AuxEvaluationPredicate
from poc.classes.AuxInbuiltValues import InbuiltValuePredicate
from poc.classes.AuxST import AuxSTOutline
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTProofArguments(AuxSTOutline, AuxInterfaceSTType, AuxEvaluationPredicate):

    def __init__(self):
        super().__init__(None, AuxSTConstants.proofArgument_root)

    def evaluate(self, sem):
        new_value = InbuiltValuePredicate(self)
        register = sem.eval_stack[-1]
        register.value = new_value
        expressions, bool_values, errors = self.evaluate_children(sem)
        new_value.set_expression(z3.And(expressions))
        if True in errors:
            new_value.set_undetermined()
        else:
            ret = True
            for bool_value in bool_values:
                ret = ret and bool_value
                if not ret:
                    break
            new_value.set_to(ret)
        return

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline
        return self._long_id
