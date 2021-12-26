from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextPredicate(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = None
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Predicate"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "CompoundPredicate":
            self.predicate = parsing_info.predicate
        elif rule == "PrimePredicate":
            self.predicate = parsing_info.predicate

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPredicate(i)
        i.parse_list.append(new_info)

