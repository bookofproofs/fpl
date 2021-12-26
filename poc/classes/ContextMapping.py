from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTType import AuxSTType


class ContextMapping(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.image = AuxSTType(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Mapping"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "To":
            self.stop_aggregation = True
        elif rule == "VariableType":
            self.image.set_type(parsing_info)
            self.image.make()

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextMapping(i)
        i.parse_list.append(new_info)
