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
        self.id = AuxSTConstants.index_value
        self.type_pattern |= AuxBits.indexBit
        self.type_pattern |= AuxBits.inbuiltBit


class InbuiltGeneric(AuxInbuiltType):
    def __init__(self, node, identifier):
        super().__init__(node)
        self.id = identifier
        self.type_pattern = AuxBits.templateBit


class InbuiltExtension(AuxInbuiltType):
    def __init__(self, node):
        super().__init__(node)
        self.id = node.id
        self.type_pattern = AuxBits.extensionBit


class InbuiltClassInstance(AuxInbuiltType):
    """ This class is a (multi-type) generic representation of all classes definable in FPL. """

    def __init__(self, constructor):
        super().__init__(constructor)
        self.id = constructor.parent.parent.id
        self.type_pattern = AuxBits.classBit
