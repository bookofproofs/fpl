from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextAll(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTPredicate(AuxSymbolTable.predicate_all, i)
        self._i = i
        self.predicate.bound_vars = []
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["All"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "VariableList":
            for var in reversed(parsing_info.var_list):
                self.predicate.bound_vars.append(var.var.id)
        elif rule == "ParenthesisedPredicate":
            self.predicate.register_child(parsing_info.predicate)
        elif rule == "all":
            self.predicate.zfrom = self._i.corrected_position('all')
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextAll(i)
        new_info.predicate.zto = i.last_positions_by_rule['All'].pos_to_str()
        i.parse_list.append(new_info)
