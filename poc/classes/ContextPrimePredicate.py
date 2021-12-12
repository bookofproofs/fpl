from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextPrimePredicate(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.predicate = None
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["PrimePredicate"] + ["Assignee"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        self.id = parsing_info.id
        if rule == "PredicateWithArguments":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "QualifiedIdentifier":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "Statement":
            self.predicate = parsing_info.statement  # noqa
        elif rule == "Identifier":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "IsOperator":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "true":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "false":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "UndefinedHeader":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "ArgumentParam":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "extDigit":
            self.predicate = AuxSTPredicate(AuxSymbolTable.extDigit, parsing_info)
            self.predicate.id = parsing_info.get_cst()

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        p_info = ContextPrimePredicate(i.parse_list, parsing_info)
        i.parse_list.append(p_info)
