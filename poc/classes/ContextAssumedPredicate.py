"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTProofArgument import AuxSTProofArgument


class ContextAssumedPredicate(AuxInterpretation):
    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.proof_argument = AuxSTProofArgument(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["AssumedPredicate"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "AssumeHeader":
            self.proof_argument.type = "assume"
            self.stop_aggregation = True
        elif rule == "PremiseOrOtherPredicate":
            self.proof_argument.register_child(parsing_info.predicate)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextAssumedPredicate(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
