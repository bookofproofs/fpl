from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxBits import AuxBits


class GeneralType(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.id = ""
        self.mod = None
        self.symbol_node = None  # this will become a pointer to the class if the GeneralType is a derived Type
        self.pattern_int = 0
        self.aggregate_previous_rules(parse_list,
                                      ["CallModifier", "Type", "TypeWithCoord", "Plus", "Star", "object", "obj",
                                       "ObjectHeader", "index", "ind", "IndexHeader"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "CallModifier":
            self.mod = parsing_info.id
        elif rule == "Type":
            self.id = parsing_info.id
            self.pattern_int = parsing_info.pattern_int
        elif rule in ["index", "ind"]:
            self.pattern_int = self.pattern_int | AuxBits.isIndex
            self.id = parsing_info.id
