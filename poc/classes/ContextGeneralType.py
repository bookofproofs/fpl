from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxBits import AuxBits
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextGeneralType(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.generalType = AuxSTType(i)
        self.generalType.type_mod = None
        self.generalType.type_pattern = 0
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["GeneralType"] +
                                      AuxRuleDependencies.dep["CallModifier"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule in ["CallModifier"]:
            self.generalType.type_mod = parsing_info.get_cst()
        elif rule == "Type":
            self.generalType.id = parsing_info.id  # noqa
            self.generalType.type_pattern = parsing_info.type_pattern  # noqa
        elif rule == "TypeWithCoord":
            for node in parsing_info.rangeOrCoord.children:  # noqa
                self.generalType.register_child(node)
        elif rule in ["IndexHeader"]:
            self.generalType.id = parsing_info.id
            self.generalType.type_pattern = 0
            self.generalType.type_pattern = self.generalType.type_pattern | AuxBits.isIndex

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextGeneralType(i)
        i.parse_list.append(new_info)

