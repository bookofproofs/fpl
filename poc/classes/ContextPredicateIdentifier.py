from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextPredicateIdentifier(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["PredicateIdentifier"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "IdStartsWithCap":
            self.id = parse_info.get_cst()
        elif rule == "AliasedId":
            self.id = parse_info.get_cst()

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPredicateIdentifier(i)
        i.parse_list.append(new_info)
