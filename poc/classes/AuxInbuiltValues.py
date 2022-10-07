from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate
from poc.classes.AuxSTType import AuxSTType


class AuxInbuiltValue:
    def __init__(self, node):
        self._copied_path = tuple()
        if node is not None:
            if hasattr(node, "zfrom"):
                self.zfrom = node.zfrom
            if hasattr(node, "zto"):
                self.zto = node.zto
            if hasattr(node, "path"):
                self._copied_path = node.path
        self._value = None
        self._declared_type = None

    def get_value(self):
        return self._value

    def set_declared_type(self, declared_type):
        self._declared_type = declared_type

    def get_declared_type(self):
        return self._declared_type


class InbuiltValueUndefined(AuxInbuiltValue):
    def __init__(self, node):
        super().__init__(node)
        self._value = AuxSTConstants.undefined
        self.set_declared_type(InbuiltUndefined(node))

    def get_value(self):
        return self._value


class InbuiltValueNamedUndefined(AuxInbuiltValue):
    def __init__(self, node, identifier: str):
        super().__init__(node)
        self._value = identifier
        self.set_declared_type(InbuiltUndefined(node))


class InbuiltValuePredicate(AuxInbuiltValue):
    def __init__(self, node):
        super().__init__(node)
        self.set_undetermined()
        self.set_declared_type(InbuiltPredicate(node))

    def set_undetermined(self):
        self._value = AuxSTConstants.undetermined

    def set_true(self):
        self._value = True

    def set_false(self):
        self._value = False

    def set_to(self, value: bool):
        self._value = value


class InbuiltValueAtRuntime(AuxInbuiltValue):
    def __init__(self, node, type_node: AuxSTType):
        super().__init__(node)
        self._value = type_node.id
        self.set_declared_type(type_node)
