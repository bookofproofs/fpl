from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTConstants import AuxSTConstants


class ContextExists(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTPredicate(AuxSTConstants.predicate_exists, i)
        self.predicate.bound_vars = []
        self.predicate.exists_number = -1  # later semantics 'at least one', can be overwritten by user
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Exists"] + AuxRuleDependencies.dep["ExistsTimesN"] +
                                      AuxRuleDependencies.dep["ExistsHeader"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Digit":
            self.predicate.exists_number = int(parsing_info.get_cst())
        elif rule == "VariableList":
            for var in reversed(parsing_info.var_list):
                self.predicate.bound_vars.append(var.var.id)
        elif rule == "ParenthesisedPredicate":
            self.predicate.register_child(parsing_info.predicate)
        elif rule == "ex":
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextExists(i)
        new_info.predicate.zto = i.last_positions_by_rule['Exists'].pos_to_str()
        new_info.predicate.zfrom = i.corrected_position('ex')
        i.parse_list.append(new_info)
