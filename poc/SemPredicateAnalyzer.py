from anytree import PostOrderIter
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTConstants import AuxSTConstants

"""
The class SemPredicateAnalyzer prepares all AuxSTPredicate nodes in the symbol table to be used for semantical
evaluation. This preparation includes, among other the formal check, if each predicate is formally correct 
(e.g., if it binds only variables that are yet unbound)
 
"""


class SemPredicateAnalyzer:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def pre_process_predicates(self):
        globals_node = AuxSymbolTable.get_child_by_outline(self.analyzer.symbol_table_root, AuxSTConstants.globals)
        for child in globals_node.children:
            # we need the predicates in the post order in the symbol table to make sure that we process
            # children before we process parents
            all_predicates = [node for node in
                              PostOrderIter(child.reference,
                                            filter_=lambda n: hasattr(n, AuxSTConstants.predicate_state))]
            for predicate in all_predicates:
                predicate.get_state().initialize()
