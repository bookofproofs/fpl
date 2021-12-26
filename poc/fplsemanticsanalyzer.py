from anytree import AnyNode
from poc.classes.AuxSymbolTable import AuxSymbolTable


class SemanticsAnalyser:

    def __init__(self, theory_name: str, syntax_tree_root: AnyNode):
        self._main_theory_node = AuxSymbolTable.get_child_by_outline(AuxSymbolTable.theory)
        pass

    def semantic_analysis(self):
        """
        Semantic analysis
        :return:
        """
        self.gather_namespaces()


    def gather_namespaces(self):
        """
        From the syntax tree Enhance the syntax tree by any used namespace.
        At the same time, construct a tree of used namespaces
        :return:
        """
        pass