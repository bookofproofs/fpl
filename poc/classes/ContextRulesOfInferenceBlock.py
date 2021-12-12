from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextRulesOfInferenceBlock(AuxInterpretation):
    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.rules_of_inference = []
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["RulesOfInferenceBlock"] +
                                      AuxRuleDependencies.dep["RuleOfInferenceList"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "InferenceHeader":
            self.stop_aggregation = True
        elif rule == "RuleOfInference":
            self.rules_of_inference.append(parsing_info.rule_of_inference)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextRulesOfInferenceBlock(i.parse_list, parsing_info)
        for ri in reversed(new_info.rules_of_inference):
            AuxSymbolTable.add_inference_rule_to_theory(i.theory_node, ri)
        i.parse_list.append(new_info)
