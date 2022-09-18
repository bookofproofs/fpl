"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTConstants import AuxSTConstants


class ContextExclusiveOr(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTPredicate(AuxSTConstants.predicate_exclusiveOr, i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["ExclusiveOr"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Predicate":
            self.predicate.register_child(parsing_info.predicate)
        elif rule == "xor":
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextExclusiveOr(i)
        new_info.predicate.zto = i.last_positions_by_rule['ExclusiveOr'].pos_to_str()
        new_info.predicate.zfrom = i.corrected_position('xor')
        # order the children like they appear the FPL source code, not like they were parsed
        new_info.predicate.children = reversed(new_info.predicate.children)
        i.parse_list.append(new_info)

