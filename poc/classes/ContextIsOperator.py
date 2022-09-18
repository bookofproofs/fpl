from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxSTStatement import AuxSTStatement


class ContextIsOperator(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTStatement(AuxSTConstants.statement_is, i)
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["IsOperator"] + ["IdStartsWithSmallCase"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Identifier":
            self.predicate.register_child(parsing_info.predicate)
        elif rule == "IndexValue":
            self.predicate.register_child(parsing_info.predicate)  # noqa
        elif rule == "GeneralType":
            self.predicate.register_child(parsing_info.generalType)  # noqa
        elif rule == "IdStartsWithSmallCase":
            if hasattr(self.predicate, "reference") and hasattr(self.predicate, "referenced_type"):
                self.stop_aggregation = True
        elif rule == "is":
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextIsOperator(i)
        new_info.predicate.children = reversed(new_info.predicate.children)
        i.parse_list.append(new_info)
