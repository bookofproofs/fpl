from poc.classes.AuxST import AuxST
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxInbuiltValues import InbuiltValueUndefined
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTExt(AuxST, AuxInterfaceSTType):
    def __init__(self, extension_id, i):
        AuxST.__init__(self, extension_id, i)
        AuxInterfaceSTType.__init__(self)
        self._constructor_node = None

    def set_constructor(self, constructor_node):
        self._constructor_node = constructor_node

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline + "." + self.id
        return self._long_id

    def evaluate(self, sem):
        if isinstance(self._declared_type, InbuiltUndefined):
            sem.eval_stack[-1].value = InbuiltValueUndefined(self)
        else:
            expected_type = self.get_declared_type()
            ret = EvaluateParams.evaluate_recursion(sem, self._constructor_node, expected_type)
            if ret.evaluation_error:
                sem.eval_stack[-1].value = InbuiltValueUndefined(self)
            else:
                sem.eval_stack[-1].value = ret.value

    def get_declared_type(self):
        if self._declared_type is None:
            self._declared_type = self._constructor_node.parent.parent.get_declared_type()
        return self._declared_type
