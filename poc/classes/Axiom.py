from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class Axiom(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.predicate = None
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["Axiom"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "AxiomHeader":
            self.stop_aggregation = True
        elif rule == "Signature":
            pass
        elif rule == "AxiomBlock":
            self.predicate = parsing_info.predicate
