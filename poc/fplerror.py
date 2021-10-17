from poc.classes.AuxAstInfo import AuxAstInfo
from poc.fplmessage import FplInterpreterMessage


class FplVariableDuplicateInVariableList(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, var_name: str):
        FplInterpreterMessage.__init__(self, var_name + " was already listed", info.line, info.col)
        self.mainType = "W"  # Warning


class FplIdentifierAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, identifier: str, info: AuxAstInfo, existing_info: AuxAstInfo):
        FplInterpreterMessage.__init__(self, "Identifier " + str(identifier) +
                                       " already defined at (" +
                                       str(existing_info.line) + "," + str(existing_info.col) + ")",
                                       info.line,
                                       info.col)


class FplMisspelledConstructor(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, expected: str, got: str):
        FplInterpreterMessage.__init__(self, "Misspelled constructor " + str(got) +
                                       " (must be named " + expected + ")",
                                       info.line,
                                       info.col)


class FplWrongPropertyName(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, parent_name: str, property_name: str):
        FplInterpreterMessage.__init__(self, "Property " + property_name +
                                       " must have a different name from its parent " + parent_name + ")",
                                       info.line,
                                       info.col)
