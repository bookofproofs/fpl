"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTProof import AuxSTProof


class ContextProof(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.building_block = AuxSTProof(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Proof"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "ProofHeadHeader":
            self.stop_aggregation = True
        elif rule == "ReferencingIdentifier":
            self.building_block.id = parsing_info.id  # noqa
        elif rule == "ProofBlock":
            self.building_block.register_child(parsing_info.variable_spec)  # noqa
            self.building_block.register_child(parsing_info.proof_arguments)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextProof(i)
        i.parse_list.append(new_info)

