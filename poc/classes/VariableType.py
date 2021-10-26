from poc.classes.AuxInterpretation import AuxInterpretation


class VariableType(AuxInterpretation):

    def __init__(self, parse_list: list, inter: AuxInterpretation):
        self.clone(inter)
        self.generalType = None
        self.paramTuple = None
        self.aggregate_previous_rules(parse_list, ['GeneralType', 'ParenthesisedGeneralType'],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "GeneralType":
            self.generalType = parse_info
        elif rule == "ParenthesisedGeneralType":
            self.generalType = parse_info.generalType
            self.paramTuple = parse_info.paramTuple
