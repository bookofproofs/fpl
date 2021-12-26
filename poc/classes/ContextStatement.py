"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextStatement(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.statement = None
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Statement"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PythonDelegate":
            self.statement = parsing_info.statement  # noqa
        elif rule == "CaseStatement":
            self.statement = parsing_info.statement  # noqa
        elif rule == "AssertionStatement":
            self.statement = parsing_info.statement  # noqa
        elif rule == "AssignmentStatement":
            self.statement = parsing_info.statement  # noqa
        elif rule == "RangeStatement":
            self.statement = parsing_info.statement  # noqa
        elif rule == "LoopStatement":
            self.statement = parsing_info.statement  # noqa
        elif rule == "ReturnStatement":
            self.statement = parsing_info.statement  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextStatement(i)
        i.parse_list.append(new_info)


