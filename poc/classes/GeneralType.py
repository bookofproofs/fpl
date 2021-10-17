from poc.classes.AuxInterpretation import AuxInterpretation


class GeneralType(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.id = ""
        self.isGeneric = False
        self.callModifier = None
        self.hasCoord = False
        self.inBuilt = False

        self.aggregate_previous_rules(parse_list,
                                      ["CallModifier", "Type", "IndexHeader", "TypeWithCoord", "Colon", "obj",
                                       "ObjectHeader", "object"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "CallModifier":
            self.callModifier = parse_info.id
        elif rule == "Type":
            self.id = parse_info.id
            self.isGeneric = parse_info.isGeneric
            self.inBuilt = parse_info.inBuilt
