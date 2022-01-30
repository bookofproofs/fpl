"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTTranslation import AuxSTTranslation


class ContextTranslation(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.transl = AuxSTTranslation(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Translation"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Tilde":
            self.stop_aggregation = True
        elif rule == "LanguageCode":
            self.transl.lang = parsing_info.get_cst()
        elif rule == "EBNFTransl":
            self.transl.register_child(parsing_info.ebnf_transl)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextTranslation(i)
        i.parse_list.append(new_info)