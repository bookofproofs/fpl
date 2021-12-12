from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTDefinitionFunctionalTerm import AuxSTDefinitionFunctionalTerm


class ContextDefinitionFunctionalTerm(AuxInterpretation):
    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.building_block = AuxSTDefinitionFunctionalTerm(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["DefinitionFunctionalTerm"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "FunctionalTermSignature":
            self.building_block.register_child(parsing_info.image)  # noqa
            self.building_block.id = parsing_info.signature.to_string()  # noqa
            self.building_block.register_child(parsing_info.signature)  # noqa
        elif rule == "FunctionalTermDefinitionBlock":
            self.building_block.register_child(parsing_info.property_list)  # noqa
            self.building_block.register_child(parsing_info.variable_spec)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextDefinitionFunctionalTerm(i.parse_list, parsing_info)
        new_info.building_block.children = reversed(new_info.building_block.children)
        i.parse_list.append(new_info)
