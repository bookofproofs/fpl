from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTPredicate import AuxSTPredicate


class ContextTrueFalse(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        if i.ast_info.cst == "true":
            p = AuxSTPredicate(AuxSymbolTable.predicate_true, i)
            p.zto = i.last_positions_by_rule['true'].pos_to_str()
            p.zfrom = i.corrected_position('true')
        elif i.ast_info.cst == "false":
            p = AuxSTPredicate(AuxSymbolTable.predicate_false, i)
            p.zto = i.last_positions_by_rule['false'].pos_to_str()
            p.zfrom = i.corrected_position('false')
        else:
            raise NotImplementedError(str(i.ast_info.cst))
        self.predicate = p

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "IdStartsWithSmallCase":
            self.id = parsing_info.get_cst()
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextTrueFalse(i)
        new_info.aggregate_previous_rules(i.parse_list, ["IdStartsWithSmallCase"], new_info.rule_aggregator)
        i.parse_list.append(new_info)
