from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSTType import AuxSTType
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextGeneralType(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)  # noqa
        self.generalType = AuxSTType(i)
        self.generalType.type_mod = None
        self.generalType.type_pattern = 0
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["GeneralType"] +
                                      AuxRuleDependencies.dep["CallModifier"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule in ["CallModifier"]:
            self.generalType.type_mod = parsing_info.get_cst()
            parsing_info.zfrom.correct_offset(1)
            self.generalType.zfrom = str(parsing_info.zfrom)
        elif rule == "Type":
            self.generalType.id = parsing_info.id  # noqa
            self.generalType.type_pattern = parsing_info.type_pattern  # noqa
            self.generalType.zfrom = str(parsing_info.zfrom)
        elif rule == "TypeWithCoord":
            if parsing_info.type is not None:  # noqa
                self.generalType.id = parsing_info.type.id  # noqa
                self.generalType.type_pattern = parsing_info.type.type_pattern  # noqa
                self.generalType.zfrom = parsing_info.type.zfrom
            self.generalType.register_child(parsing_info.rangeOrCoord)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextGeneralType(i)
        new_info.generalType.zto = i.last_positions_by_rule['GeneralType'].pos_to_str()
        i.parse_list.append(new_info)
