from poc.classes.AuxInterpretation import AuxInterpretation


class GeneralType(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.id = ""
        self.generic = False
        self.callModifier = None
        self.hasCoord = False
        self.inBuilt = False
        self.isIndex = False
        self.isSyntaxExtension = False
        self.aggregate_previous_rules(parse_list,
                                      ["CallModifier", "Type", "TypeWithCoord", "Plus", "Star", "object", "obj",
                                       "ObjectHeader", "index", "ind", "IndexHeader"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "CallModifier":
            self.callModifier = parsing_info.id
        elif rule == "Type":
            self.id = parsing_info.id
            self.generic = parsing_info.generic
            self.inBuilt = parsing_info.inBuilt
            self.isSyntaxExtension = parsing_info.isSyntaxExtension
        elif rule in ["index", "ind"]:
            self.inBuilt = True
            self.isIndex = True
            self.id = parsing_info.id
