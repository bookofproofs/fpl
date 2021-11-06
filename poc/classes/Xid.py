from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class Xid(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["XId"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule in AuxRuleDependencies.dep["XId"]:
            self.id = parsing_info.id + self.id
