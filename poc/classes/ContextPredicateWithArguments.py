"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSTPredicateWithArgs import AuxSTPredicateWithArgs
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextPredicateWithArguments(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.predicate = AuxSTPredicateWithArgs(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["PredicateWithArguments"] +
                                      AuxRuleDependencies.dep["PredicateList"], self.rule_aggregator)

        self.predicate.children = reversed(self.predicate.children)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Identifier":
            self.predicate.id = parsing_info.predicate.id  # noqa
            self.stop_aggregation = True
        elif rule == "Predicate":
            self.predicate.register_child(parsing_info.predicate)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPredicateWithArguments(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
