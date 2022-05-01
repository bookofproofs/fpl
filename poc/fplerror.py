from poc.classes.AuxAstInfo import AuxAstInfo
from poc.fplmessage import FplInterpreterMessage


class FplVariableDuplicateInVariableList(FplInterpreterMessage):
    def __init__(self, var, other, file_name: str):
        v_s = var.zfrom.split(".")
        other_s = other.zfrom.split(".")
        super().__init__(
            "Variable '{0}' already listed at {1}:{2}".format(var.id, other_s[0], str(int(other_s[1]) + 1)),
            v_s[0], str(int(v_s[1]) + 1), file_name)
        self.mainType = "W"  # Warning
        self.diagnose_id = "SE0010"


class FplIdentifierAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, identifier: str, zfrom: str, file: str, existing_zfrom: str, existing_file: str):
        zfrom_split = zfrom.split(".")
        existing_zfrom_split = existing_zfrom.split(".")
        if existing_file == file:
            if (int(zfrom_split[0]) > int(existing_zfrom_split[0])) or \
                    (int(zfrom_split[0]) == int(existing_zfrom_split[0]) and
                     int(zfrom_split[1]) > int(existing_zfrom_split[1])):
                super().__init__("Identifier '{0}' already defined at ({1},{2})".format(identifier,
                                                                                        existing_zfrom_split[0],
                                                                                        existing_zfrom_split[1]),
                                 zfrom_split[0],
                                 zfrom_split[1],
                                 file)
            else:
                super().__init__("Identifier '{0}' already defined at ({1},{2})".format(identifier,
                                                                                        zfrom_split[0],
                                                                                        zfrom_split[1]),
                                 existing_zfrom_split[0],
                                 existing_zfrom_split[1],
                                 file)
        else:
            super().__init__("Identifier '{0}' already defined at {1}({2},{3})".format(identifier,
                                                                                       existing_file,
                                                                                       zfrom_split[0],
                                                                                       zfrom_split[1]),
                             existing_zfrom_split[0],
                             existing_zfrom_split[1],
                             file)

        self.diagnose_id = "SE0020"


class FplMisspelledConstructor(FplInterpreterMessage):
    def __init__(self, class_name: str, constr_name: str, zfrom: str, file_name: str):
        s = zfrom.split(".")
        super().__init__(
            "Misspelled constructor '{0}' of class '{1}' (must be the same)".format(constr_name, class_name),
            s[0],
            s[1],
            file_name)
        self.diagnose_id = "SE0030"


class FplMisspelledProperty(FplInterpreterMessage):
    def __init__(self, prop_name: str, main_name: str, main_type: int, zfrom: str, file_name: str):
        s = zfrom.split(".")
        if main_type == 1:
            main_type_name = "class"
        elif main_type == 2:
            main_type_name = "predicate"
        elif main_type == 3:
            main_type_name = "functional term"
        else:
            main_type_name = "definition"

        super().__init__(
            "Misspelled property '{0}' of {1} '{2}' (must be different)".format(main_name, main_type_name, prop_name),
            s[0],
            s[1],
            file_name)
        self.diagnose_id = "SE0035"


class FplMalformedGlobalId(FplInterpreterMessage):
    def __init__(self, identifier: str, namespace: str, zfrom: str, file_name: str):
        s = zfrom.split(".")
        super().__init__(
            "The identifier '{0}' should not conflict with the namespace '{1}'".format(identifier, namespace),
            s[0],
            s[1],
            file_name)
        self.mainType = "W"  # Warning
        self.diagnose_id = "SE0040"


class FplInvalidInheritance(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, base_class_name: str, what: str):
        super().__init__("Inheritance from '{0}' not possible (not a defined class but {1} type)".format(
            base_class_name, what),
            info.line,
            info.col,
            info.file)
        self.diagnose_id = "SE0050"


class FplAliasConflict(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, alias: str, other: AuxAstInfo):
        super().__init__(
            "The alias '{0}' already used at {1}({2},{3})".format(alias, other.file, other.line, other.col),
            info.line,
            info.col,
            info.file)
        self.diagnose_id = "SE0060"


class FplUndeclaredVariable(FplInterpreterMessage):
    def __init__(self, zfrom: str, var_name: str, file_name: str):
        s = zfrom.split(".")
        super().__init__("The variable '{0}' was not declared in the current context".format(var_name),
                         s[0], s[1], file_name)
        self.diagnose_id = "SE0070"


class FplUnusedVariable(FplInterpreterMessage):
    def __init__(self, zfrom: str, var_name: str, file_name: str):
        s = zfrom.split(".")
        super().__init__(
            "The variable '{0}' (declared at ({1},{2}) was not used in the current context".format(var_name, s[0],
                                                                                                   str(int(s[1]) + 1)),
            s[0], s[1], file_name)
        self.mainType = "W"  # Warning
        self.diagnose_id = "SE0075"


class FplVariableAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, zfrom: str, other_zfrom: str, var_name: str, file_name: str):
        s = zfrom.split(".")
        s_other = other_zfrom.split(".")
        super().__init__("The variable '{0}' was already declared in the current context at ({1},{2})".format(
            var_name, s_other[0], int(s_other[1]) + 1), s[0], str(int(s[1]) + 1),
            file_name)
        self.diagnose_id = "SE0080"


class FplIdentifierNotDeclared(FplInterpreterMessage):
    def __init__(self, identifier: str, file_name: str, zfrom: str):
        s = zfrom.split(".")
        super().__init__("Undeclared identifier '{0}'".format(identifier), s[0], s[1], file_name)
        self.diagnose_id = "SE0090"


class FplIdentifierAmbiguous(FplInterpreterMessage):
    def __init__(self, info: AuxAstInfo, class_name: str, found_nodes: tuple):
        global_names = []
        for c in found_nodes:
            global_names.append(c.gid + " ({0})".format(c.outline))
        names = ",".join(global_names)
        super().__init__("Ambiguous identifier '{0}'. Found in ({1})".format(class_name, names),
                         info.line, info.col,
                         info.file)
        self.diagnose_id = "SE0100"


class FplNamespaceNotFound(FplInterpreterMessage):
    def __init__(self, namespace: str, file: str, zfrom: str):
        pos = zfrom.split(".")
        super().__init__("Namespace '{0}' not found".format(namespace), pos[0], pos[1], file)
        self.diagnose_id = "SE0110"


class FplMalformedNamespace(FplInterpreterMessage):
    def __init__(self, namespace: str, file: str):
        super().__init__("The namespace '{0}' should consist of different names".format(namespace),
                         1,
                         1,
                         file)
        self.diagnose_id = "SE0120"
