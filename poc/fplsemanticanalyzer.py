from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplIdentifierAlreadyDeclared
from poc.fplerror import FplMalformedNamespace


class SemanticAnalyser:

    def __init__(self, symbol_table_root: AnyNode, errors: list):
        self._symbol_table_root = symbol_table_root
        self._errors = errors
        pass

    def semantic_analysis(self):
        """
        Semantic analysis
        :return:
        """
        self._check_theories()
        self._check_duplicate_identifiers()

    def _check_theories(self):
        loaded_theories = AuxSymbolTable.get_theories(self._symbol_table_root)
        for theory in loaded_theories:
            self.__check_namespace_identifiers(theory)
            self.__check_malformed_namespace(theory)

    def __check_namespace_identifiers(self, theory):
        """
        Check if all namespaces are listed only once in the the uses clause of each theory
        :return: None
        """
        duplicate_checker = dict()
        uses_node = AuxSymbolTable.get_child_by_outline(theory, AuxSymbolTable.uses)
        for child in uses_node.children:
            if child.id not in duplicate_checker:
                duplicate_checker[child.id] = child
            else:
                self._errors.append(
                    FplIdentifierAlreadyDeclared(child.id, child.zfrom, theory.file_name,
                                                 duplicate_checker[child.id].zfrom,
                                                 theory.file_name))

    def __check_malformed_namespace(self, theory):
        """
        Check if each loaded namespace consists of different names separated by a dot
        :return: None
        """
        duplicate_checker = set()
        namespace_split = theory.namespace.split(".")
        for chunk in namespace_split:
            if chunk not in duplicate_checker:
                duplicate_checker.add(chunk)
            else:
                self._errors.append(FplMalformedNamespace(theory.namespace,theory.file_name))

    def _check_duplicate_identifiers(self):
        """
        Check if all global identifiers are unique
        :return: None
        """
        globals_node = AuxSymbolTable.get_child_by_outline(self._symbol_table_root, AuxSymbolTable.globals)
        duplicate_checker = dict()
        for child in globals_node.children:
            if child.gid not in duplicate_checker:
                duplicate_checker[child.gid] = child
            else:
                node = child.reference
                theory_node = child.theory
                if node.outline != AuxSymbolTable.classDefaultConstructor:
                    existing_node = duplicate_checker[child.gid].reference
                    existing_theory_node = duplicate_checker[child.gid].theory
                    self._errors.append(
                        FplIdentifierAlreadyDeclared(child.id, node.zfrom, theory_node.file_name, existing_node.zfrom,
                                                     existing_theory_node.file_name))

