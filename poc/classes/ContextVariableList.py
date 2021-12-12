from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.ContextVariable import ContextVariable
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextVariableList(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.var_list = []
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["VariableList"] + ["Assignee"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Variable":
            self.var_list.append(parsing_info)
        elif rule == "Assignee":
            # cast the Assignee to Variable and append it to the named variable declaration
            var = ContextVariable([], parsing_info)
            var.var = parsing_info.predicate
            self.var_list.append(var)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextVariableList(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
