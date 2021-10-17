from poc.classes.AuxInterpretation import AuxInterpretation


class NamespaceIdentifier(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      ["IdStartsWithCap", "Dot"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        # concatenate specific proceeding rules
        if rule in ["IdStartsWithCap", "Dot"]:
            self.id = parse_info.id + self.id
