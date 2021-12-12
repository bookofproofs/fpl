from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextParenthesisedGeneralType(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.generalType = None
        self.paramTuple = None
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["ParenthesisedGeneralType"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "GeneralType":
            self.generalType = parse_info.generalType
        elif rule == "ParamTuple":
            self.paramTuple = parse_info

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        param_tuple = ContextParenthesisedGeneralType(i.parse_list, parsing_info)
        i.parse_list.append(param_tuple)

