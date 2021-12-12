from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTRuleOfInference import AuxSTRuleOfInference


class ContextRuleOfInference(AuxInterpretation):
    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.rule_of_inference = AuxSTRuleOfInference(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["RuleOfInference"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Signature":
            parsing_info.symbol_signature.make()
            self.rule_of_inference.register_child(parsing_info.symbol_signature)
            self.rule_of_inference.id = parsing_info.symbol_signature.to_string()
        elif rule == "PremiseConclusionBlock":
            self.rule_of_inference.register_child(parsing_info.con)
            self.rule_of_inference.register_child(parsing_info.pre)
            self.rule_of_inference.register_child(parsing_info.variable_spec)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextRuleOfInference(i.parse_list, parsing_info)
        new_info.rule_of_inference.children = reversed(new_info.rule_of_inference.children)
        i.parse_list.append(new_info)
