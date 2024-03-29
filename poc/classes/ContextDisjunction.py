"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTConstants import AuxSTConstants


class ContextDisjunction(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTPredicate(AuxSTConstants.predicate_disjunction, i)
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["Disjunction"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PredicateList":
            for pinfo in parsing_info.prd_list:  # noqa
                self.predicate.register_child(pinfo.predicate)
        elif rule == "or":
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextDisjunction(i)
        new_info.predicate.zto = i.last_positions_by_rule['Disjunction'].pos_to_str()
        new_info.predicate.zfrom = i.corrected_position('or')
        i.parse_list.append(new_info)
