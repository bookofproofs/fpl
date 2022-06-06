class AuxBits:
    classBit = 0
    objectBit = 1
    predicateBit = 2
    functionalTermBit = 4
    typeBit = objectBit + predicateBit + functionalTermBit
    templateBit = 8
    inbuiltBit = 16
    extensionBit = 32
    indexBit = 64
    hasCoordBit = 128

    @staticmethod
    def is_class(pattern_int: int):
        return pattern_int == 0

    @staticmethod
    def is_inbuilt_object(pattern_int: int):
        return (pattern_int & AuxBits.objectBit) > 0 and (pattern_int & AuxBits.inbuiltBit) > 0

    @staticmethod
    def is_object(pattern_int: int):
        return (pattern_int & AuxBits.objectBit) > 0

    @staticmethod
    def is_predicate(pattern_int: int):
        return (pattern_int & AuxBits.predicateBit) > 0

    @staticmethod
    def is_functional_term(pattern_int: int):
        return (pattern_int & AuxBits.functionalTermBit) > 0

    @staticmethod
    def is_generic(pattern_int: int):
        return (pattern_int & AuxBits.templateBit) > 0

    @staticmethod
    def is_extension(pattern_int: int):
        return (pattern_int & AuxBits.extensionBit) > 0

    @staticmethod
    def is_index(pattern_int: int):
        return (pattern_int & AuxBits.indexBit) > 0

    @staticmethod
    def has_coord(pattern_int: int):
        return (pattern_int & AuxBits.hasCoordBit) > 0

    @staticmethod
    def is_inbuilt(pattern_int: int):
        return (pattern_int & AuxBits.inbuiltBit) > 0

    @staticmethod
    def is_type(pattern_int: int):
        return (pattern_int & AuxBits.typeBit) > 0
