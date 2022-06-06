from poc.classes.AuxSymbolTable import AuxSymbolTable


class InbuiltType:
    def __init__(self, identifier):
        self.id = identifier

    def get_qualified_id(self):
        return self.id

    def get_type_signature(self):
        return self.id


class InbuiltUndefined(InbuiltType):
    def __init__(self):
        super().__init__(AuxSymbolTable.undefined)


class InbuiltPredicate(InbuiltType):
    def __init__(self):
        super().__init__(AuxSymbolTable.predicate)


class InbuiltFunctionalTerm(InbuiltType):
    def __init__(self):
        super().__init__(AuxSymbolTable.functionalTerm)


class InbuiltIndex(InbuiltType):
    def __init__(self):
        super().__init__(AuxSymbolTable.index_value)


class InbuiltGeneric(InbuiltType):
    def __init__(self, identifier):
        super().__init__(AuxSymbolTable.generic)
        self.id = identifier


class InbuiltObject(InbuiltType):
    def __init__(self):
        super().__init__(AuxSymbolTable.obj)


class InbuiltExtension(InbuiltType):
    def __init__(self, identifier):
        super().__init__(AuxSymbolTable.obj)
        self.id = identifier
