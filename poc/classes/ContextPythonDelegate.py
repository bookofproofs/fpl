"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTStatementPyDel import AuxSTStatementPyDel


class ContextPythonDelegate(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.statement = AuxSTStatementPyDel(i)
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["PythonDelegate"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "py":
            self.stop_aggregation = True
        elif rule == "PythonIdentifier":
            self.statement.id = parsing_info.get_cst()
        elif rule == "PredicateList":
            for pinfo in parsing_info.prd_list:  # noqa
                self.statement.register_child(pinfo.predicate)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPythonDelegate(i)
        i.parse_list.append(new_info)
