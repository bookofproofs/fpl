"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTProofArgument import AuxSTProofArgument
from poc.classes.AuxSTProofStop import AuxSTProofStop


class ContextDerivedPredicate(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.proof_argument = AuxSTProofArgument(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["DerivedPredicate"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Predicate":
            self.proof_argument.register_child(parsing_info.predicate)  # noqa
        elif rule == "qed":
            qed = AuxSTProofStop()
            qed.type = rule
            self.proof_argument.register_child(qed)
        elif rule == "trivial":
            qed = AuxSTProofStop()
            qed.type = rule
            self.proof_argument.register_child(qed)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextDerivedPredicate(i)
        i.parse_list.append(new_info)
