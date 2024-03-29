"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTLocalization import AuxSTLocalization


class ContextLocalization(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.localization = AuxSTLocalization(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Localization"] +
                                      AuxRuleDependencies.dep["TranslationList"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Predicate":
            self.localization.register_child(parsing_info.predicate)  # noqa
            self.stop_aggregation = True
        elif rule == "Translation":
            self.localization.register_child(parsing_info.transl)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextLocalization(i)
        new_info.localization.children = reversed(new_info.localization.children)
        i.parse_list.append(new_info)
