from poc.classes.AuxInterpretation import AuxInterpretation


class ParamTuple(AuxInterpretation):

    def __init__(self, parse_list: list, inter: AuxInterpretation):
        self.clone(inter)
        self.tuple = []
        self.aggregate_previous_rules(parse_list,
                                      ['NamedVariableDeclaration', 'LeftParen', 'RightParen',
                                       'NamedVariableDeclarationList'],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "NamedVariableDeclaration":
            self.tuple.append(parse_info)
