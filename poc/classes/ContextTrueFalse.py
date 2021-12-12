from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTPredicate import AuxSTPredicate


class ContextTrueFalse(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        if parsing_info.get_ast_info().cst == "true":
            p = AuxSTPredicate(AuxSymbolTable.predicate_true, parsing_info)
        elif parsing_info.get_ast_info().cst == "false":
            p = AuxSTPredicate(AuxSymbolTable.predicate_false, parsing_info)
        else:
            raise NotImplementedError(str(parsing_info.get_ast_info().cst))

        self.predicate = p
        parsing_info.aggregate_previous_rules(parse_list, ["IdStartsWithSmallCase"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "IdStartsWithSmallCase":
            self.id = parsing_info.get_cst()
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        p_info = ContextTrueFalse(i.parse_list, parsing_info)
        i.parse_list.append(p_info)
