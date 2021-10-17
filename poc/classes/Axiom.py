from poc.classes.AuxInterpretation import AuxInterpretation


class Axiom(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      ["axiom", "ax", "postulate", "post", "AxiomHeader"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        pass
