"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxPredicate import AuxPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable


class Disjunction(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.info = parsing_info
        self.predicate = AuxPredicate(AuxSymbolTable.predicate_disjunction)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["Disjunction"] + AuxRuleDependencies.dep["PredicateList"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Predicate":
            self.predicate.register_child(parsing_info.predicate)
        elif rule == "or":
            self.stop_aggregation = True
