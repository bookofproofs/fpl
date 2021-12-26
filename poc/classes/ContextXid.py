from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextXid(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["XId"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule in AuxRuleDependencies.dep["XId"]:
            self.id = parsing_info.get_cst() + self.id

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        type_info = ContextXid(i)
        i.parse_list.append(type_info)
