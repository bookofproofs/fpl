"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTProofArgument import AuxSTProofArgument


class ContextProofArgument(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.proof_argument = AuxSTProofArgument(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["ProofArgument"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "ArgumentIdentifier":
            self.proof_argument.id = parsing_info.id  # noqa
            self.stop_aggregation = True
        elif rule == "Justification":
            self.proof_argument.register_child(parsing_info.justification)  # noqa
        elif rule == "ArgumentInference":
            for child in parsing_info.proof_argument.children:
                child.parent = self.proof_argument

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextProofArgument(i)
        new_info.proof_argument.zfrom = i.corrected_position('ArgumentIdentifier')
        new_info.proof_argument.zto = i.last_positions_by_rule['ProofArgument'].pos_to_str()
        i.parse_list.append(new_info)

