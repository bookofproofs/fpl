import traceback
from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.SemCheckerIdentifiers import SemCheckerIdentifiers
from poc.fplerror import FplErrorManager, FplIdentifierAlreadyDeclared, FplMalformedNamespace
from poc.fplmessage import FplInterpreterSystemError


class SemanticAnalyser:

    def __init__(self, symbol_table_root: AnyNode, error_mgr: FplErrorManager):
        self.symbol_table_root = symbol_table_root
        self.error_mgr = error_mgr
        self.loaded_theories = AuxSymbolTable.get_theories(self.symbol_table_root)
        self.globals_node = AuxSymbolTable.get_child_by_outline(self.symbol_table_root, AuxSymbolTable.globals)
        self.sem_checker_identifiers = SemCheckerIdentifiers(self)

    def semantic_analysis(self):
        """
        Semantic analysis
        :return:
        """
        if AuxISourceAnalyser.verbose:
            self._check_theories()
            self.sem_checker_identifiers.analyse()
        else:
            # in non-verbose mode, we handle all exceptions 'user-friendly' as not to cause the main loop to halt
            try:
                self._check_theories()
                self.sem_checker_identifiers.analyse()
            except Exception:  # noqa
                # add any exceptions during the semantic analysis into the regular error list
                self.error_mgr.add_error(
                    FplInterpreterSystemError(
                        traceback.format_exc().replace("Traceback (most recent call last):\n  ", "")))

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
