"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser


class ContextRightBound(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.bound_included = True
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["RightBound"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "ExclamationMark":
            self.bound_included = False

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextRightBound(i)
        i.parse_list.append(new_info)



