import z3
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInbuiltTypes import InbuiltUndefined, InbuiltPredicate, InbuiltIndex
from poc.classes.AuxInterfaceSTType import AuxInterfaceSTType
from poc.classes.AuxSTType import AuxSTType


class AuxInbuiltValue(AuxInterfaceSTType):
    def __init__(self, node):
        super().__init__()
        self._copied_path = tuple()
        if node is not None:
            if hasattr(node, "zfrom"):
                self.zfrom = node.zfrom
            if hasattr(node, "zto"):
                self.zto = node.zto
            if hasattr(node, "path"):
                self._copied_path = node.path
        self._value = None
        self._expression = None
        self._satisfiable = None
        self._satisfiability_check_done = False
        self._model = None

    def get_value(self):
        return self._value

    def get_expression(self):
        if self._expression is None:
            self._expression = z3.Bool(self.get_long_id())
        return self._expression

    def set_expression(self, expression):
        self._expression = expression

    def get_long_id(self):
        return str(self._value)

    def is_satisfiable(self):
        self._determine_satisfiability()
        return self._satisfiable

    def _determine_satisfiability(self):
        if not self._satisfiability_check_done:
            # determine satisfiability if the check has never been done yet
            s = z3.Solver()
            s.add(self.get_expression())
            if s.check() == z3.sat:
                self._satisfiable = True
                self._model = s.model()
            else:
                self._satisfiable = False
            # mark satisfiability as determined
            self._satisfiability_check_done = True


class InbuiltValueUndefined(AuxInbuiltValue):

    def __init__(self, node):
        super().__init__(node)
        self._value = AuxSTConstants.undefined
        self.set_declared_type(InbuiltUndefined(node))


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


class InbuiltValueInteger(AuxInbuiltValue):
    def __init__(self, node):
        super().__init__(node)
        self.set_declared_type(InbuiltIndex(node))

    def set_value(self, value):
        self._value = int(value)
