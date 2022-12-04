from poc.classes.AuxST import AuxST
from poc.classes.AuxInbuiltTypes import InbuiltUndefined
from poc.classes.AuxInbuiltValues import InbuiltValueUndefined
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType


class AuxSTExt(AuxST, AuxInterfaceSTType):
    def __init__(self, extension_id, i):
        AuxST.__init__(self, extension_id, i)
        AuxInterfaceSTType.__init__(self)
        self._class_node = None

    def set_class(self, class_node):
        self._class_node = class_node

    def get_long_id(self):
        if self._long_id is None:
            self._long_id = self.outline + "." + self.id
        return self._long_id

    def evaluate(self, sem):
        if isinstance(self._declared_type, InbuiltUndefined):
            sem.eval_stack[-1].value = InbuiltValueUndefined(self)
        else:
            raise NotImplementedError()

    def get_declared_type(self):
        if self._declared_type is None:
            self._declared_type = self._class_node.get_declared_type()
        return self._declared_type
