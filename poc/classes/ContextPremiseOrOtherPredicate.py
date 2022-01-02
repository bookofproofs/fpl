"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextPremiseOrOtherPredicate(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self._i = i
        self.predicate = None
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["PremiseOrOtherPredicate"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PremiseHeader":
            self.predicate = AuxSTPredicate(AuxSymbolTable.preReferenced, self._i)
        elif rule == "Predicate":
            self.predicate = parsing_info.predicate  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPremiseOrOtherPredicate(i)
        i.parse_list.append(new_info)

