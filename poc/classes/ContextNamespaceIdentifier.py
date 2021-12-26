from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextNamespaceIdentifier(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["NamespaceIdentifier"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "IdStartsWithCap":
            self.id = parsing_info.get_cst() + self.id
        elif rule == "Dot":
            self.id = parsing_info.get_cst() + self.id

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextNamespaceIdentifier(i)
        i.parse_list.append(new_info)
