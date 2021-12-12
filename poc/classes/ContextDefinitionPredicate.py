from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate


class ContextDefinitionPredicate(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.building_block = AuxSTDefinitionPredicate(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["DefinitionPredicate"] +
                                      AuxRuleDependencies.dep["PredicateHeader"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule in AuxRuleDependencies.dep["PredicateHeader"]:
            self.stop_aggregation = True
        elif rule == "Signature":
            self.building_block.register_child(parsing_info.symbol_signature)  # noqa
            self.building_block.id = parsing_info.symbol_signature.to_string()
        elif rule == "PredicateDefinitionBlock":
            self.building_block.register_child(parsing_info.property_list)  # noqa
            self.building_block.register_child(parsing_info.predicate)  # noqa
            self.building_block.register_child(parsing_info.variable_spec)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextDefinitionPredicate(i.parse_list, parsing_info)
        new_info.building_block.children = reversed(new_info.building_block.children)
        i.parse_list.append(new_info)
