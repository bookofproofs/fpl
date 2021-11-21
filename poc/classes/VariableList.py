from poc.classes.AuxInterpretation import AuxInterpretation


class VariableList(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.var_list = []
        self.aggregate_previous_rules(parse_list,
                                      ['IdStartsWithSmallCase', 'Variable', 'Comma', 'IW', 'Entity', 'Assignee'],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "Variable":
            self.var_list.append(parse_info)
        elif rule == "Assignee":
            self.var_list.append(parse_info.entity.variable)
