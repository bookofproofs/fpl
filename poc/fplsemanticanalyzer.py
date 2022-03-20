from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.fplerror import FplIdentifierAlreadyDeclared
from poc.classes.AuxSTBlockWithSignature import AuxSTBlockWithSignature
from poc.classes.AuxSTInstance import AuxSTInstance
from poc.classes.AuxSTClass import AuxSTClass
from poc.classes.AuxSTConstructor import AuxSTConstructor


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
        self._check_namespace_identifiers()
        self._check_duplicate_identifiers()

    def _check_namespace_identifiers(self):
        """
        Check if all namespaces are listed only once in the the uses clause of each theory
        :return: None
        """
        loaded_theories = AuxSymbolTable.get_theories(self._symbol_table_root)
        for theory in loaded_theories:
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

    def _check_duplicate_identifiers(self):
        globals_node = AuxSymbolTable.get_child_by_outline(self._symbol_table_root, AuxSymbolTable.globals)
        duplicate_checker = dict()
        for child in globals_node.children:
            if child.gid not in duplicate_checker:
                duplicate_checker[child.gid] = child
            else:
                node = child.reference
                if node.outline != AuxSymbolTable.classDefaultConstructor:
                    existing_node = duplicate_checker[child.gid].reference
                    theory_node = SemanticAnalyser.__get_theory(node)
                    theory_existing = SemanticAnalyser.__get_theory(existing_node)
                    self._errors.append(
                        FplIdentifierAlreadyDeclared(child.id, node.zfrom, theory_node.file_name, existing_node.zfrom,
                                                     theory_existing.file_name))

    @staticmethod
    def __get_theory(node):
        node_type = type(node)
        if issubclass(node_type, AuxSTBlockWithSignature):
            return node.parent.parent
        elif issubclass(node_type, AuxSTInstance):
            return node.parent.parent.parent.parent
        elif node_type is AuxSTClass:
            return node.parent.parent
        elif node_type is AuxSTConstructor and node.outline != AuxSymbolTable.classDefaultConstructor:
            return node.parent.parent.parent.parent
        else:
            return None
