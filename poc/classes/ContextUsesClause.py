from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable
from anytree import AnyNode


class ContextUsesClause(AuxInterpretation):
    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.used_namespaces = []
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["UsesClause"] +
                                      AuxRuleDependencies.dep["WildcardTheoryNamespaceList"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "WildcardTheoryNamespace":
            self.used_namespaces.append(parsing_info.used_namespace)  # noqa

    @ staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextUsesClause(i.parse_list, parsing_info)
        uses_node = AuxSymbolTable.get_child_by_outline(i.theory_node, AuxSymbolTable.uses)
        for used_namespace in new_info.used_namespaces:
            used_namespace.parent = uses_node
        i.parse_list.append(new_info)
