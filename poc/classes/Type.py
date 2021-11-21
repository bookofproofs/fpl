from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxBits import AuxBits


class Type(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.pattern_int = 0
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
            self.pattern_int = self.pattern_int | AuxBits.isObject
            self.pattern_int = self.pattern_int | AuxBits.isGeneric
            self.id = parsing_info.id + self.id
        elif rule in ["Digit", "Dot", "At", "ext"]:
            self.id = parsing_info.id + self.id
        elif rule in ["PredicateIdentifier", "IdStartsWithCap"] and not self._colon_read:
            # colon_read prevents mixing up PredicateIdentifiers of classes with their types
            self.pattern_int = self.pattern_int | AuxBits.isObject
            self.id = parsing_info.id
        elif rule in ["obj", "object"]:
            self.pattern_int = self.pattern_int | AuxBits.isObject
            self.pattern_int = self.pattern_int | AuxBits.isInbuilt
            self.id = parsing_info.id
        elif rule in ["func", "function"]:
            self.pattern_int = self.pattern_int | AuxBits.isFunctionalTerm
            self.pattern_int = self.pattern_int | AuxBits.isInbuilt
            self.id = parsing_info.id
        elif rule in ["pred", "predicate"]:
            self.pattern_int = self.pattern_int | AuxBits.isPredicate
            self.pattern_int = self.pattern_int | AuxBits.isInbuilt
            self.id = parsing_info.id
        elif rule == "Colon":
            self._colon_read = True
        elif rule == "XId":
            self.pattern_int = self.pattern_int | AuxBits.isExtension
            self.id = parsing_info.id


