from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.fplmessage import FplInterpreterMessage


class FplErrorManager:
    def __init__(self):
        self._errors = set()

    def add_error(self, error: FplInterpreterMessage):
        if error not in self._errors:
            self._errors.add(error)

    def get_errors(self):
        return self._errors

    def clear_errors(self):
        self._errors.clear()

    def print_errors(self):
        if len(self._errors) > 0:
            print(str(len(self._errors)), "errors found:")
            for err in self._errors:
                print(err)
        else:
            print("Congratulations! No errors found")

    def has_errors(self):
        return len(self._errors) > 0

    def remove_file_errors(self, file_name: str):
        new_set = set(filter(lambda x: x.file == file_name, self._errors))
        self._errors.clear()
        self._errors = new_set


class FplVariableDuplicateInVariableList(FplInterpreterMessage):
    def __init__(self, var, other, file_name: str):
        v_s = var.zfrom.split(".")
        other_s = other.zfrom.split(".")
        super().__init__(
            "Variable '{0}' already listed at {1}:{2}".format(var.id, other_s[0], str(int(other_s[1]) + 1)),
            v_s[0], v_s[1], file_name)
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
    def __init__(self, class_name: str, constr_name: str, node):
        s = node.reference.zfrom.split(".")
        super().__init__(
            "Misspelled constructor '{0}' of class '{1}' (must be the same)".format(constr_name, class_name),
            s[0],
            s[1],
            node.theory.file_name)
        self.diagnose_id = "SE0030"


class FplMisspelledProperty(FplInterpreterMessage):
    def __init__(self, prop_name: str, main_name: str, node):
        s = node.reference.zfrom.split(".")
        main_type_name = node.reference.get_node_type_str()
        super().__init__(
            "Misspelled property '{0}' of {1} '{2}' (must be different)".format(main_name, main_type_name, prop_name),
            s[0],
            s[1],
            node.theory.file_name)
        self.diagnose_id = "SE0035"


class FplMalformedGlobalId(FplInterpreterMessage):
    def __init__(self, identifier: str, node):
        s = node.reference.zfrom.split(".")
        super().__init__(
            "The identifier '{0}' should not conflict with the namespace '{1}'".format(identifier,
                                                                                       node.theory.namespace),
            s[0],
            s[1],
            node.theory.file_name)
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
            "The variable '{0}' was not used in the current context".format(var_name),
            s[0], s[1], file_name)
        self.mainType = "W"  # Warning
        self.diagnose_id = "SE0075"


class FplVariableAlreadyDeclared(FplInterpreterMessage):
    def __init__(self, zfrom: str, other_zfrom: str, var_name: str, file_name: str):
        s = zfrom.split(".")
        s_other = other_zfrom.split(".")
        super().__init__("The variable '{0}' was already declared in the current context at ({1},{2})".format(
            var_name, s_other[0], int(s_other[1]) + 1), s[0], s[1], file_name)
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


class FplTemplateMisused(FplInterpreterMessage):
    def __init__(self, template: str, zfrom: str, file_name: str):
        s = zfrom.split(".")
        super().__init__("The generic type '{0}' cannot be used in this context".format(template),
                         s[0], s[1], file_name)
        self.diagnose_id = "SE0130"


class FplMissingProof(FplInterpreterMessage):
    def __init__(self, block):
        s = block.reference.zfrom.split(".")
        super().__init__("The theorem_like statement '{0}' lacks a proof".format(block.reference.id),
                         s[0], s[1], block.theory.file_name)
        self.mainType = "W"  # Warning
        self.diagnose_id = "SE0140"


class FplProvedConjecture(FplInterpreterMessage):
    def __init__(self, proof, conjecture):
        s = conjecture.reference.zfrom.split(".")
        if proof.theory.file_name != conjecture.theory.file_name:
            super().__init__(
                "Proof '{0}' (in {1}) of conjecture '{2}' detected".format(proof.reference.id,
                                                                           proof.theory.file_name,
                                                                           conjecture.reference.id) +
                " (change to a new possible theorem)",
                s[0], s[1], conjecture.theory.file_name)
        else:
            super().__init__(
                "Proof '{0}' of conjecture '{1}' detected".format(proof.reference.id,
                                                                  conjecture.reference.id) +
                " (change to a new possible theorem)",
                s[0], s[1], conjecture.theory.file_name)
        self.diagnose_id = "SE0150"


class FplProofMissingTheoremLikeStatement(FplInterpreterMessage):
    def __init__(self, referenced_theorem_like_statement: str, block):
        s = block.reference.zfrom.split(".")
        super().__init__(
            "Theorem-like statement '{0}' not found for proof '{1}'".format(referenced_theorem_like_statement,
                                                                            block.reference.id),
            s[0], s[1], block.theory.file_name)
        self.diagnose_id = "SE0160"


class FplCorollaryMissingTheoremLikeStatement(FplInterpreterMessage):
    def __init__(self, referenced_theorem_like_statement: str, block):
        s = block.reference.zfrom.split(".")
        super().__init__(
            "Theorem-like statement '{0}' not found for corollary '{1}'".format(referenced_theorem_like_statement,
                                                                                block.reference.id),
            s[0], s[1], block.theory.file_name)
        self.diagnose_id = "SE0165"


class FplAmbiguousSignature(FplInterpreterMessage):
    def __init__(self, first, second):
        first_s = first.reference.zfrom.split(".")
        second_s = second.reference.zfrom.split(".")
        if first.theory.file_name != second.theory.file_name:
            super().__init__(
                "Ambiguous blocks {0} and {1} with the ".format(first.reference.get_node_type_str(),
                                                                second.reference.get_node_type_str()) +
                "same signature '{0}' (other at {1}:{2})".format(second.reference.id, second.theory.file_name,
                                                                 first_s[0] + "," +
                                                                 str(int(first_s[1]) + 1)),
                second_s[0], second_s[1], first.theory.file_name)
        else:
            super().__init__("Ambiguous blocks {0} and {1} with the ".format(first.reference.get_node_type_str(),
                                                                             second.reference.get_node_type_str()) +
                             "same signature '{0}' (other at {1})".format(second.reference.id,
                                                                          first_s[0] + "," +
                                                                          str(int(first_s[1]) + 1)),
                             second_s[0], second_s[1], first.theory.file_name)

        self.diagnose_id = "SE0170"


class FplForbiddenOverride(FplInterpreterMessage):
    def __init__(self, first, second):
        first_s = first.reference.zfrom.split(".")
        second_s = second.reference.zfrom.split(".")
        if first.theory.file_name != second.theory.file_name:
            super().__init__(
                "'{0}' ({1}) and ".format(first.reference.id, first.reference.get_node_type_str()) +
                "'{0}' ({1}) cannot coexist in theory (other at {2}:{3})".format(second.reference.id,
                                                                                 second.reference.get_node_type_str(),
                                                                                 second.theory.file_name,
                                                                                 second_s[0] + "," + str(
                                                                                     int(second_s[1]) + 1)),
                first_s[0], first_s[1], first.theory.file_name)
        else:
            super().__init__(
                "'{0}' ({1}) and ".format(first.reference.id, first.reference.get_node_type_str()) +
                "'{0}' ({1}) cannot coexist in theory (other at {2})".format(second.reference.id,
                                                                             second.reference.get_node_type_str(),
                                                                             second_s[0] + "," + str(
                                                                                 int(second_s[1]) + 1)),
                first_s[0], first_s[1], first.theory.file_name)

        self.diagnose_id = "SE0180"


class FplCrossNamespaceAmbiguity(FplInterpreterMessage):
    def __init__(self, first, second):
        first_s = first.reference.zfrom.split(".")
        second_s = second.reference.zfrom.split(".")
        super().__init__(
            "'{0}' ({1}) and '{2}' ({3}, ".format(first.reference.id, first.reference.get_node_type_str(),
                                                  second.reference.id, second.reference.get_node_type_str()) +
            "{0} at {1}({2},{3})) conflict, consider using an alias".format(second.theory.namespace,
                                                                            second.theory.file_name,
                                                                            second_s[0],
                                                                            str(int(second_s[1]) + 1)),
            first_s[0], first_s[1], first.theory.file_name)
        self.diagnose_id = "SE0190"


class FplTypeNotAllowed(FplInterpreterMessage):
    def __init__(self, type_node, zfrom, file_name):
        first_s = type_node.reference.zfrom.split(".")
        second_s = zfrom.split(".")
        if file_name == type_node.theory.file_name:
            super().__init__(
                "'{0}' ({1}, found at {2},{3}) not allowed as a type".format(type_node.reference.id,
                                                                             type_node.reference.get_node_type_str(),
                                                                             first_s[0],
                                                                             str(int(first_s[1]) + 1)),
                second_s[0], second_s[1], file_name
            )
        else:
            super().__init__(
                "'{0}' ({1}, found at {2}({3},{4})) not allowed as a type".format(type_node.reference.id,
                                                                                  type_node.reference.get_node_type_str(),
                                                                                  type_node.theory.file_name,
                                                                                  first_s[0],
                                                                                  str(int(first_s[1]) + 1)),
                second_s[0], second_s[1], file_name
            )
        self.diagnose_id = "SE0200"


class FplWrongArguments(FplInterpreterMessage):
    def __init__(self, arguments: list(), expected_arguments: list, node):
        s = node.zfrom.split(".")
        one_of = ""
        if len(expected_arguments) > 1:
            one_of = " one of"
        msg = "Wrong arguments {0}, expected{1} {2}".format(str(arguments), one_of, " or ".join(expected_arguments))

        super().__init__(msg.replace("'", "").replace("[", "(").replace("]", ")"),
                         s[0], s[1], node.path[1].file_name
                         )
        self.diagnose_id = "SE0220"


class FplVariableNotInitialized(FplInterpreterMessage):
    def __init__(self, var):
        s = var.zfrom.split(".")
        super().__init__("Variable '{0}' neither initialized nor bound".format(var.id), s[0], s[1],
                         var.path[1].file_name)
        self.diagnose_id = "SE0230"


class FplAxiomNotSatisfiable(FplInterpreterMessage):
    def __init__(self, axiom):
        s = axiom.zfrom.split(".")
        super().__init__("Axiom '{0}' not satisfiable".format(axiom.id), s[0], s[1],
                         axiom.path[1].file_name)
        self.diagnose_id = "SE0240"


class FplPremiseNotSatisfiable(FplInterpreterMessage):
    def __init__(self, premise_node):
        s = premise_node.zfrom.split(".")
        super().__init__("Premise of '{0}' not satisfiable".format(premise_node.parent.id), s[0], s[1],
                         premise_node.path[1].file_name)
        self.diagnose_id = "SE0245"


class FplTypeMismatch(FplInterpreterMessage):
    def __init__(self, node, expected, actual):
        s = node.zfrom.split(".")
        if hasattr(node, AuxSTConstants.copied_path):
            path = node._copied_path
        else:
            path = node.path
        super().__init__("Type mismatch: expected '{0}', received '{1}' in this context".format(expected, actual),
                         s[0], s[1],
                         path[1].file_name)
        self.diagnose_id = "SE0250"


class FplPredicateRecursion(FplInterpreterMessage):
    def __init__(self, node, node_recursion_occurred):
        s = node_recursion_occurred.zfrom.split(".")
        super().__init__("Cannot evaluate recursive predicates in '{0}'".format(node.id),
                         s[0], s[1],
                         node_recursion_occurred.path[1].file_name)
        self.diagnose_id = "SE0260"


class FplVariableBound(FplInterpreterMessage):
    def __init__(self, var_id, quantor, already_bounding_node):
        s = quantor.zfrom.split(".")
        b = already_bounding_node.zfrom.split(".")
        super().__init__("Variable '{0}' already bound at ({1},{2})".format(var_id, b[0], str(int(b[1]) + 1)),
                         s[0], s[1],
                         quantor.path[1].file_name)
        self.diagnose_id = "SE0270"


class FplCircularReference(FplInterpreterMessage):
    def __init__(self, class_node, list_references: list):
        s = class_node.zfrom.split(".")
        msg = "Circular reference found '{0}'".format(str(list_references))
        msg = msg.replace("'", "")
        super().__init__(
            msg,
            s[0], s[1],
            class_node.path[1].file_name)
        self.diagnose_id = "SE0280"
