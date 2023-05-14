"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTIdentifier import AuxSTIdentifier


class ContextIdentifier(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTIdentifier(i)
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Identifier"] +
                                      ["VariableList", "VariableSpecificationList"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PredicateIdentifier":
            # wrap the identifier for the symbol table
            self.predicate.id = parsing_info.id
            self.predicate.zfrom = str(parsing_info.zfrom)
            self.predicate.zto = str(parsing_info.zto)
            self.stop_aggregation = True
        elif rule == "Assignee":
            self.predicate = parsing_info.predicate  # noqa
            if not hasattr(self.predicate, "id"):
                if self.predicate is not None:
                    if hasattr(self.predicate, "set_id"):
                        self.predicate.set_id("")  # assignees must have an id, even if anonymous
            self.stop_aggregation = True
        elif rule == "VariableList":
            self.predicate = parsing_info.var_list[0].var  # noqa
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextIdentifier(i)
        i.parse_list.append(new_info)
