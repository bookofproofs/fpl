from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ParenthesisedGeneralType(AuxInterpretation):

    def __init__(self, parse_list: list, inter: AuxInterpretation):
        self.clone(inter)
        self.generalType = None
        self.paramTuple = None
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["ParenthesisedGeneralType"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "GeneralType":
            self.generalType = parse_info
        elif rule == "ParamTuple":
            self.paramTuple = parse_info
        elif rule == "IW":
            pass
