class AuxBits:
    isClass = 0
    isObject = 1
    isPredicate = 2
    isFunctionalTerm = 4
    isTemplate = 8
    isInbuilt = 16
    isGeneric = 32
    isExtension = 64
    isIndex = 128
    hasCoord = 256

    @staticmethod
    def is_class(pattern_int: int):
        return pattern_int == 0

    @staticmethod
    def is_object(pattern_int: int):
        return (pattern_int & AuxBits.isObject) > 0

    @staticmethod
    def is_predicate(pattern_int: int):
        return (pattern_int & AuxBits.isPredicate) > 0

    @staticmethod
    def is_functional_term(pattern_int: int):
        return (pattern_int & AuxBits.isFunctionalTerm) > 0

    @staticmethod
    def in_built(pattern_int: int):
        return (pattern_int & AuxBits.isInbuilt) > 0

    @staticmethod
    def is_generic(pattern_int: int):
        return (pattern_int & AuxBits.isGeneric) > 0

    @staticmethod
    def is_extension(pattern_int: int):
        return (pattern_int & AuxBits.isExtension) > 0

    @staticmethod
    def is_index(pattern_int: int):
        return (pattern_int & AuxBits.isIndex) > 0

    @staticmethod
    def has_coord(pattern_int: int):
        return (pattern_int & AuxBits.hasCoord) > 0
