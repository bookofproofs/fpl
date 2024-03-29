"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSTRange import AuxSTRange
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextRangeInType(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.range = AuxSTRange(i)
        self._counter = 1
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["RangeInType"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "CoordInType":
            self.range.register_child(parsing_info.predicate)  # noqa
            if self._counter == 2:
                self.range.zto = parsing_info.predicate.zto  # noqa
                self.stop_aggregation = True
            else:
                self.range.zfrom = parsing_info.predicate.zfrom  # noqa
        elif rule == "Tilde":
            self._counter += 1

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextRangeInType(i)
        new_info.range.children = reversed(new_info.range.children)
        i.parse_list.append(new_info)

