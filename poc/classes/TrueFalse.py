from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxPredicate import AuxPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable


class TrueFalse(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.info = parsing_info
        if parsing_info.id == "true":
            p = AuxPredicate(AuxSymbolTable.predicate_true)
        elif parsing_info.id == "false":
            p = AuxPredicate(AuxSymbolTable.predicate_false)
        else:
            raise NotImplementedError(str(parsing_info.id))

        self.predicate = p
        parsing_info.aggregate_previous_rules(parse_list, ["IdStartsWithSmallCase"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "IdStartsWithSmallCase":
            self.id = parsing_info.get_cst()
            self.stop_aggregation = True

