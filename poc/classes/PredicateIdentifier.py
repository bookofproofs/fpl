from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class PredicateIdentifier(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["PredicateIdentifier"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "IdStartsWithCap":
            self.id = parse_info.id
        elif rule == "AliasedId":
            self.id = parse_info.id
