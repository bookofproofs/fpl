from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.SemCheckerIdentifiers import SemCheckerIdentifiers
from poc.fplerror import FplErrorManager
from poc.fplerror import FplIdentifierAlreadyDeclared
from poc.fplerror import FplMalformedNamespace


class SemanticAnalyser:

    def __init__(self, symbol_table_root: AnyNode, error_mgr: FplErrorManager):
        self._symbol_table_root = symbol_table_root
        self.error_mgr = error_mgr
        self.loaded_theories = AuxSymbolTable.get_theories(self._symbol_table_root)
        self.globals_node = AuxSymbolTable.get_child_by_outline(self._symbol_table_root, AuxSymbolTable.globals)
        self.sem_checker_identifiers = SemCheckerIdentifiers(self)

    def semantic_analysis(self):
        """
        Semantic analysis
        :return:
        """
        self._check_theories()
        self.sem_checker_identifiers.analyse()

    def _check_theories(self):
        for theory in self.loaded_theories:
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
                self.error_mgr.add_error(
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
                self.error_mgr.add_error(FplMalformedNamespace(theory.namespace, theory.file_name))
