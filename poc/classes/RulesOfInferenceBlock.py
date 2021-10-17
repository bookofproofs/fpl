from poc.classes.AuxInterpretation import AuxInterpretation


class RulesOfInferenceBlock(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      ["InferenceHeader", "inference", "inf", "LeftBrace", "RightBrace"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        # ignore all proceeding rules
        pass
