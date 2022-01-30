"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTSelf import AuxSTSelf
from poc.classes.AuxSTArgs import AuxSTArgs


class ContextPredicateWithArguments(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTPredicateWithArgs(i)
        self._args = AuxSTArgs(i)
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["PredicateWithArguments"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Identifier":
            if type(parsing_info.predicate) is AuxSTSelf:
                zto = self.predicate.zto
                self.predicate = parsing_info.predicate  # noqa
                self.predicate.zto = zto
            else:
                self.predicate.zfrom = parsing_info.predicate.zfrom  # noqa
                self.predicate.id = parsing_info.predicate.id  # noqa
            self.predicate.register_child(self._args)
            self.stop_aggregation = True
        elif rule == "LeftParen":
            parsing_info.zfrom.correct_offset(1)
            self._args.zfrom = str(parsing_info.zfrom)
        elif rule == "RightParen":
            parsing_info.zto.correct_offset(1)
            self.predicate.zto = str(parsing_info.zto)
        elif rule == "PredicateList":
            for p_info in parsing_info.prd_list:  # noqa
                self._args.register_child(p_info.predicate)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPredicateWithArguments(i)
        i.parse_list.append(new_info)