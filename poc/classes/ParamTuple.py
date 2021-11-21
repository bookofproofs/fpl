from poc.classes.AuxInterpretation import AuxInterpretation


class ParamTuple(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.tuple = []
        self.aggregate_previous_rules(parse_list,
                                      ['NamedVariableDeclaration', 'LeftParen', 'RightParen',
                                       'NamedVariableDeclarationList'],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "NamedVariableDeclaration":
            self.tuple.append(parse_info)
        elif rule == "LeftParen":
            self.stop_aggregation = True
