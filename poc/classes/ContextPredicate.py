from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextPredicate(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.predicate = None
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["Predicate"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "CompoundPredicate":
            self.predicate = parsing_info.predicate
        elif rule == "PrimePredicate":
            self.predicate = parsing_info.predicate

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        p_info = ContextPredicate(i.parse_list, parsing_info)
        i.parse_list.append(p_info)

