from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTClassInstance import AuxSTClassInstance


class ContextClassInstance(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.building_block = AuxSTClassInstance(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["ClassInstance"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "VariableType":
            self.building_block.register_child(parsing_info.var_type)  # noqa
        elif rule == "Signature":
            self.building_block.register_child(parsing_info.symbol_signature)  # noqa
            self.building_block.id = parsing_info.symbol_signature.to_string()  # noqa
        elif rule == "InstanceBlock":
            self.building_block.register_child(parsing_info.variable_spec)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextClassInstance(i)
        new_info.building_block.children = reversed(new_info.building_block.children)
        i.parse_list.append(new_info)
