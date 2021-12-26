"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextClosedOrOpenRange(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.range = None
        self._right_included = False
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["ClosedOrOpenRange"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "LeftBound":
            self.range.left_included = parsing_info.bound_included  # noqa
            self.stop_aggregation = True
        elif rule == "Range":
            self.range = parsing_info.range  # noqa
            self.range.right_included = self._right_included
        elif rule == "RightBound":
            self._right_included = parsing_info.bound_included  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextClosedOrOpenRange(i)
        i.parse_list.append(new_info)

