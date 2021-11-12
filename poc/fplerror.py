from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxAstInfo import AuxAstInfo
from poc.fplmessage import FplInterpreterMessage


class FplVariableDuplicateInVariableList(FplInterpreterMessage):
    def __init__(self, info: AuxInterpretation, other: AuxInterpretation):
        FplInterpreterMessage.__init__(self,
                                       "Variable " + info.id + " already listed at " + str(other.rule_line()) + ":" +
                                       str(other.rule_col()), info.rule_line(), info.rule_col(), info.rule_line())
        self.mainType = "W"  # Warning


class FplIdentifierAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, identifier: str, info: AuxAstInfo, existing_info: AuxAstInfo):
        FplInterpreterMessage.__init__(self, "Identifier " + str(identifier) +
                                       " already defined at (" +
                                       str(existing_info.line) + "," + str(existing_info.col) + ")",
                                       info.line,
                                       info.col,
                                       info.file)


class FplMisspelledConstructor(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, expected: str, got: str):
        FplInterpreterMessage.__init__(self, "Misspelled constructor " + str(got) +
                                       " (must be named " + expected + ")",
                                       info.line,
                                       info.col,
                                       info.file)


class FplMalformedGlobalId(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, global_id: str):
        FplInterpreterMessage.__init__(self, "The global id " + global_id +
                                       " should consist of different names.",
                                       info.line,
                                       info.col,
                                       info.file)


class FplInvalidInheritance(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, base_class_name: str, what: str):
        FplInterpreterMessage.__init__(self, "Inheritance from " + base_class_name +
                                       " not possible (not a defined class but " + what + ")",
                                       info.line,
                                       info.col,
                                       info.file)


class FplAliasConflict(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, alias: str, other: AuxAstInfo):
        FplInterpreterMessage.__init__(self, "The alias " + alias +
                                       " already used at " + other.file + "(" + other.line + "," + other.col + ")",
                                       info.line,
                                       info.col,
                                       info.file)


class FplUndeclaredVariable(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, var_name: str):
        FplInterpreterMessage.__init__(self, "The name '{0}' does not exist in the current context".format(var_name),
                                       info.line, info.col,
                                       info.file)
