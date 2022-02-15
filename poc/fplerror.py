from poc.classes.AuxAstInfo import AuxAstInfo
from poc.fplmessage import FplInterpreterMessage


class FplVariableDuplicateInVariableList(FplInterpreterMessage):
    def __init__(self, var, other, file_name: str):
        v_s = var.zfrom.split(".")
        other_s = other.zfrom.split(".")
        FplInterpreterMessage.__init__(self,
                                       "Variable " + var.id + " already listed at " +
                                       other_s[0] + ":" + str(int(other_s[1]) + 1),
                                       v_s[0], str(int(v_s[1]) + 1), file_name)
        self.mainType = "W"  # Warning
        self.diagnose_id = "SE0010"


class FplIdentifierAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, identifier: str, info: AuxAstInfo, existing_info: AuxAstInfo):
        FplInterpreterMessage.__init__(self, "Identifier " + str(identifier) +
                                       " already defined at (" +
                                       str(existing_info.line) + "," + str(existing_info.col) + ")",
                                       info.line,
                                       info.col,
                                       info.file)
        self.diagnose_id = "SE0020"


class FplMisspelledConstructor(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, expected: str, got: str):
        FplInterpreterMessage.__init__(self, "Misspelled constructor " + str(got) +
                                       " (must be named " + expected + ")",
                                       info.line,
                                       info.col,
                                       info.file)
        self.diagnose_id = "SE0030"


class FplMalformedGlobalId(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, global_id: str):
        FplInterpreterMessage.__init__(self, "The global id " + global_id +
                                       " should consist of different names.",
                                       info.line,
                                       info.col,
                                       info.file)
        self.diagnose_id = "SE0040"


class FplInvalidInheritance(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, base_class_name: str, what: str):
        FplInterpreterMessage.__init__(self, "Inheritance from " + base_class_name +
                                       " not possible (not a defined class but " + what + " type)",
                                       info.line,
                                       info.col,
                                       info.file)
        self.diagnose_id = "SE0050"


class FplAliasConflict(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, alias: str, other: AuxAstInfo):
        FplInterpreterMessage.__init__(self, "The alias " + alias +
                                       " already used at " + other.file + "(" + other.line + "," + other.col + ")",
                                       info.line,
                                       info.col,
                                       info.file)
        self.diagnose_id = "SE0060"


class FplUndeclaredVariable(FplInterpreterMessage):
    def __init__(self, zfrom: str, var_name: str, file_name: str):
        s = zfrom.split(".")
        FplInterpreterMessage.__init__(self, "The name '{0}' does not exist in the current context".format(var_name),
                                       s[0], s[1], file_name)
        self.diagnose_id = "SE0070"


class FplVariableAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, zfrom: str, other_zfrom: str, var_name: str, file_name: str):
        s = zfrom.split(".")
        s_other = other_zfrom.split(".")
        FplInterpreterMessage.__init__(self,
                                       "The name '{0}' was already declared in the current context at ({1},{2})".format(
                                           var_name, s_other[0], int(s_other[1]) + 1), s[0], str(int(s[1]) + 1),
                                       file_name)
        self.diagnose_id = "SE0080"


class FplIdentifierNotDeclared(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, class_name: str):
        FplInterpreterMessage.__init__(self,
                                       "Undeclared identifier '{0}'".format(class_name),
                                       info.line, info.col,
                                       info.file)
        self.diagnose_id = "SE0090"


class FplIdentifierAmbiguous(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, class_name: str, found_nodes: tuple):
        global_names = []
        for c in found_nodes:
            global_names.append(c.gid + " ({0})".format(c.outline))
        names = ",".join(global_names)
        FplInterpreterMessage.__init__(self,
                                       "Ambiguous identifier '{0}'. Found in ({1})".format(class_name, names),
                                       info.line, info.col,
                                       info.file)
        self.diagnose_id = "SE0100"


class FplNamespaceNotFound(FplInterpreterMessage):
    def __init__(self, namespace: str, file: str, zfrom: str):
        pos = zfrom.split(".")
        FplInterpreterMessage.__init__(self,
                                       "Namespace '{0}' not found".format(namespace), pos[0], pos[1], file)
        self.diagnose_id = "SE0110"
