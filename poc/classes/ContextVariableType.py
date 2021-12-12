from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTType import AuxSTType


class ContextVariableType(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.generalType = None
        self.paramTuple = None
        self.var_type = None
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["VariableType"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "GeneralType":
            self.generalType = parse_info.generalType  # noqa
        elif rule == "ParenthesisedGeneralType":
            self.generalType = parse_info.generalType  # noqa
            self.paramTuple = parse_info.paramTuple  # noqa
        self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        var_type_info = ContextVariableType(i.parse_list, parsing_info)
        var_type_info.var_type = var_type_info.generalType
        var_type_info.var_type.set_type(var_type_info)
        var_type_info.var_type.make()
        i.parse_list.append(var_type_info)
