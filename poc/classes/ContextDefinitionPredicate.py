from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate


class ContextDefinitionPredicate(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.building_block = AuxSTDefinitionPredicate(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["DefinitionPredicate"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PredicateHeader":
            self.building_block.keyword = parsing_info.id  # noqa
            self.stop_aggregation = True
        elif rule == "Signature":
            self.building_block.id = parsing_info.symbol_signature.to_string()
            parsing_info.symbol_signature.children = reversed(parsing_info.symbol_signature.children)  # noqa
            self.building_block.register_child(parsing_info.symbol_signature)  # noqa
        elif rule == "PredicateDefinitionBlock":
            self.building_block.register_child(parsing_info.property_list)  # noqa
            self.building_block.register_child(parsing_info.predicate)  # noqa
            self.building_block.register_child(parsing_info.variable_spec)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextDefinitionPredicate(i)
        new_info.building_block.children = reversed(new_info.building_block.children)
        i.parse_list.append(new_info)
