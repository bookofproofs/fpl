"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextProperty(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.building_block = None
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Property"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PropertyHeader":
            if parsing_info.id in ['mandatory', 'mand']:
                self.building_block.mandatory = True
            else:
                self.building_block.mandatory = False
            self.building_block.zfrom = self._i.corrected_position("PropertyHeader")
            self.stop_aggregation = True
        elif rule == "DefinitionProperty":
            self.building_block = parsing_info.building_block  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextProperty(i)
        i.parse_list.append(new_info)


