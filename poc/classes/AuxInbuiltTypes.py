from poc.classes.AuxBits import AuxBits
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTType import AuxSTType


class AuxInbuiltType(AuxSTType):
    def __init__(self, node):
        super().__init__(None)
        self._copied_path = tuple()
        if node is not None:
            if hasattr(node, "zfrom"):
                self.zfrom = node.zfrom
            if hasattr(node, "zto"):
                self.zto = node.zto
            if hasattr(node, "path"):
                self._copied_path = node.path


class InbuiltUndefined(AuxInbuiltType):
    def __init__(self, node):
        super().__init__(node)
        self.id = AuxSTConstants.undefined
        self.type_pattern |= AuxBits.inbuiltBit
        # the inbuilt undefined is a type of itself


class InbuiltPredicate(AuxInbuiltType):
    def __init__(self, node):
        super().__init__(node)
        self.id = AuxSTConstants.predicate
        self.type_pattern |= AuxBits.inbuiltBit
        self.type_pattern |= AuxBits.predicateBit


class InbuiltFunctionalTerm(AuxInbuiltType):
    def __init__(self, node):
        super().__init__(node)
        self.id = AuxSTConstants.functionalTerm
        self.type_pattern |= AuxBits.inbuiltBit
        self.type_pattern |= AuxBits.functionalTermBit


class InbuiltIndex(AuxInbuiltType):
    def __init__(self, node):
        super().__init__(node)
        self.id = AuxSTConstants.int
        self.type_pattern |= AuxBits.index
        self.type_pattern |= AuxBits.inbuiltBit


class InbuiltVariableVariadic(AuxInbuiltType):
    def __init__(self, node):
        super().__init__(node)
        self.id = AuxSTConstants.variadic_var
        self.type_pattern |= AuxBits.variadicBit
