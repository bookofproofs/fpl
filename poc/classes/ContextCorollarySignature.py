"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTSignature import AuxSTSignature


class ContextCorollarySignature(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.symbol_signature = AuxSTSignature(i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["CorollarySignature"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "ReferencingIdentifier":
            self.symbol_signature.set_id(parsing_info.id)
            self.stop_aggregation = True
        elif rule == "ParamTuple":
            self.symbol_signature.set_params(parsing_info.tuple)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextCorollarySignature(i)
        new_info.symbol_signature.make()
        i.parse_list.append(new_info)