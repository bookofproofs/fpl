from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation


class ContextParamTuple(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.tuple = []
        self.zfrom = ""  # remember the beginning to correct the zfrom position of any signature
        self.aggregate_previous_rules(i.parse_list,
                                      ['NamedVariableDeclaration', 'LeftParen', 'RightParen',
                                       'NamedVariableDeclarationList'],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "NamedVariableDeclaration":
            self.tuple.append(parse_info)
        elif rule == "LeftParen":
            self.zfrom = parse_info.get_ast_info().pos_to_str()
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        param_tuple = ContextParamTuple(i)
        param_tuple.tuple.reverse()
        i.parse_list.append(param_tuple)

