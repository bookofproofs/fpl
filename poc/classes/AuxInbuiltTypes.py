from poc.classes.AuxBits import AuxBits
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTType import AuxSTType


class InbuiltUndefined(AuxSTType):
    def __init__(self):
        super().__init__(None)
        self.id = AuxSymbolTable.undefined


class NamedUndefined(AuxSTType):
    def __init__(self, identifier):
        super().__init__(None)
        self.id = identifier


class InbuiltPredicate(AuxSTType):
    def __init__(self):
        super().__init__(None)
        self.id = AuxSymbolTable.predicate
        self.type_pattern = AuxBits.predicateBit


class EvaluatedPredicate(AuxSTType):
    def __init__(self, bool_value):
        super().__init__(None)
        self.id = AuxSymbolTable.predicate
        self.type_pattern = AuxBits.predicateBit
        if isinstance(bool_value, bool):
            self.set_repr(bool_value)
        else:
            AssertionError("Expected boolean value, got " + str(bool_value))


class InbuiltFunctionalTerm(AuxSTType):
    def __init__(self):
        super().__init__(None)
        self.id = AuxSymbolTable.functionalTerm
        self.type_pattern = AuxBits.functionalTermBit


class InbuiltIndex(AuxSTType):
    def __init__(self):
        super().__init__(None)
        self.id = AuxSymbolTable.index_value
        self.type_pattern = AuxBits.indexBit


class InbuiltGeneric(AuxSTType):
    def __init__(self, identifier):
        super().__init__(None)
        self.id = identifier
        self.type_pattern = AuxBits.templateBit


class InbuiltObject(AuxSTType):
    def __init__(self):
        super().__init__(None)
        self.id = AuxSymbolTable.obj
        self.type_pattern = AuxBits.inbuiltBit + AuxBits.objectBit


class InbuiltExtension(AuxSTType):
    def __init__(self, identifier):
        super().__init__(None)
        self.id = identifier
        self.type_pattern = AuxBits.extensionBit


class InbuiltClassInstance(AuxSTType):
    """ This class is a (multi-type) generic representation of all classes definable in FPL. """

    def __init__(self, constructor):
        super().__init__(None)
        self.id = constructor.parent.parent.id
        self.type_pattern = AuxBits.classBit
