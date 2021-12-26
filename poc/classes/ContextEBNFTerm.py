"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTEbnfTerm import AuxSTEbnfTerm


class ContextEBNFTerm(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.term = AuxSTEbnfTerm(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["EBNFTerm"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "EBNFFactor":
            self.term.register_child(parsing_info.factor)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextEBNFTerm(i)
        new_info.term.children = reversed(new_info.term.children)
        i.parse_list.append(new_info)
