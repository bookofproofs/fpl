from poc.classes.AuxInterpretation import AuxInterpretation


class Type(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.generic = False
        self.inBuilt = False
        self.isSyntaxExtension = False
        self._colon_read = False
        self.aggregate_previous_rules(parse_list,
                                      ["tpl", "template", "TemplateHeader", "IdStartsWithCap", "LongTemplateHeader",
                                       "obj", "object",
                                       "ObjectHeader", "Digit", "function", "func", "FunctionalTermHeader", "predicate",
                                       "pred", "Colon",
                                       "PredicateHeader", "AliasedId", "Dot", "PredicateIdentifier", "XId"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "TemplateHeader":
            self.generic = True
            self.id = parsing_info.id + self.id
        elif rule in ["Digit", "Dot", "At", "ext"]:
            self.id = parsing_info.id + self.id
        elif rule in ["PredicateIdentifier", "IdStartsWithCap"] and not self._colon_read:
            # colon_read prevents mixing up PredicateIdentifiers of classes with their types
            self.id = parsing_info.id
        elif rule in ["obj", "object", "func", "function", "pred", "predicate"]:
            self.inBuilt = True
            self.id = parsing_info.id
        elif rule == "Colon":
            self._colon_read = True
        elif rule == "XId":
            self.isSyntaxExtension = True
            self.id = parsing_info.id
