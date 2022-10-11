from poc.classes.AuxBits import AuxBits


class AuxInterfaceSTTypePattern:
    """
    A class for elements of the logic of testing for the type of an FPL type
    """

    def is_class(self):
        return self.type_pattern == 0

    def is_inbuilt_object(self):
        return (self.type_pattern & AuxBits.objectBit) > 0 and (self.type_pattern & AuxBits.inbuiltBit) > 0

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

    def is_index(self):
        return (self.type_pattern & AuxBits.indexBit) > 0

    def has_coord(self):
        return (self.type_pattern & AuxBits.hasCoordBit) > 0

    def is_inbuilt(self):
        return (self.type_pattern & AuxBits.inbuiltBit) > 0

