from poc.classes.AuxInterpretation import AuxInterpretation


class VariableType(AuxInterpretation):

    def __init__(self, parse_list: list, inter: AuxInterpretation):
        self.clone(inter)
        self.generalType = None
        self.anonymousSignature = None
        self.aggregate_previous_rules(parse_list, ['GeneralType', 'AnonymousSignature'],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "GeneralType":
            self.generalType = parse_info
        elif rule == "AnonymousSignature":
            self.anonymousSignature = parse_info
