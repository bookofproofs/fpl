from poc.classes.AuxInterpretation import AuxInterpretation


class NamespaceModifier(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.modifier = ""
        self.aggregate_previous_rules(parse_list,
                                      ["Dot", "Star", "Alias", "alias", "IdStartsWithCap"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule=="Star":
            self.modifier = "*"
        elif rule=="IdStartsWithCap":
            self.modifier = parse_info.id
