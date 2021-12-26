from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextUsesClause(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.used_namespaces = []
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["UsesClause"] +
                                      AuxRuleDependencies.dep["WildcardTheoryNamespaceList"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "WildcardTheoryNamespace":
            self.used_namespaces.append(parsing_info.used_namespace)  # noqa

    @ staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextUsesClause(i)
        uses_node = AuxSymbolTable.get_child_by_outline(i.theory_node, AuxSymbolTable.uses)
        for used_namespace in reversed(new_info.used_namespaces):
            used_namespace.parent = uses_node
        i.parse_list.append(new_info)
