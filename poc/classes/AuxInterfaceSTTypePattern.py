from poc.classes.AuxBits import AuxBits


class AuxInterfaceSTTypePattern:
    # this attribute will be added to the class by the derived classes, and
    # we add it here to avoid warnings from the IDE
    type_pattern = None

    """
    A class for the logic of testing for the type of FPL type
    """

    def is_class(self):
        return self.type_pattern == 0

    def is_inbuilt_object(self):
        return (self.type_pattern & AuxBits.objectBit) > 0 and (self.type_pattern & AuxBits.inbuiltBit) > 0

    def is_inbuilt_functional_term(self):
        return (self.type_pattern & AuxBits.functionalTermBit) > 0 and (self.type_pattern & AuxBits.inbuiltBit) > 0

    def is_inbuilt_predicate(self):
        return (self.type_pattern & AuxBits.predicateBit) > 0 and (self.type_pattern & AuxBits.inbuiltBit) > 0

    def is_object(self):
        return (self.type_pattern & AuxBits.objectBit) > 0

    def is_predicate(self):
        return (self.type_pattern & AuxBits.predicateBit) > 0

    def is_functional_term(self):
        return (self.type_pattern & AuxBits.functionalTermBit) > 0

    def is_generic(self):
        return (self.type_pattern & AuxBits.templateBit) > 0

    def is_extension(self):
        return (self.type_pattern & AuxBits.extensionBit) > 0

    def is_variadic(self):
        return (self.type_pattern & AuxBits.variadicBit) > 0

    def has_coord(self):
        return (self.type_pattern & AuxBits.hasCoordBit) > 0

    def is_inbuilt(self):
        return (self.type_pattern & AuxBits.inbuiltBit) > 0

    def is_index(self):
        return (self.type_pattern & AuxBits.index) > 0
