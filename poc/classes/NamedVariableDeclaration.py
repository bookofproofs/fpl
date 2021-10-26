from poc.classes.AuxInterpretation import AuxInterpretation


class NamedVariableDeclaration(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.var_list = dict()
        self.var_type = None
        self.aggregate_previous_rules(parse_list,
                                      ["VariableList", "VariableType", "Colon"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        # concatenate specific proceeding rules
        if rule == "VariableList":
            self.var_list = parse_info.var_list
        elif rule == "VariableType":
            self.var_type = parse_info
