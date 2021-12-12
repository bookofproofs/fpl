from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTStatement import AuxSTStatement


class ContextIsOperator(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.predicate = AuxSTStatement(AuxSymbolTable.isOperator, parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["IsOperator"] + ["IdStartsWithSmallCase"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Identifier":
            self.predicate.register_child(parsing_info.predicate)
        elif rule == "GeneralType":
            self.predicate.register_child(parsing_info.generalType)  # noqa
        elif rule == "IdStartsWithSmallCase":
            if hasattr(self.predicate, "reference") and hasattr(self.predicate, "referenced_type"):
                self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextIsOperator(i.parse_list, parsing_info)
        new_info.predicate.children = reversed(new_info.predicate.children)
        i.parse_list.append(new_info)
