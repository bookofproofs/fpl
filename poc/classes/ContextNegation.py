"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextNegation(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.predicate = AuxSTPredicate(AuxSymbolTable.predicate_negation, parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["Negation"] + ["IdStartsWithSmallCase"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "ParenthesisedPredicate":
            self.predicate.register_child(parsing_info.predicate)
        elif rule == "IdStartsWithSmallCase":
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextNegation(i.parse_list, parsing_info)
        i.parse_list.append(new_info)

