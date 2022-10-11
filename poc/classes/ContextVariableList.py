from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.ContextVariable import ContextVariable
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextVariableList(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.var_list = []
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["VariableList"] + ["Assignee", "Identifier"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Variable":
            self.var_list.append(parsing_info)
        elif rule in ["Assignee", "Identifier"]:
            # cast the Assignee to Variable and append it to the named variable declaration
            var = ContextVariable(self._i)
            var.var = parsing_info.predicate
            self.var_list.append(var)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextVariableList(i)
        i.parse_list.append(new_info)
