from poc.classes.AuxInterpretation import AuxInterpretation


class WildcardTheoryNamespace(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        self.clone(parsing_info)
        self.modifier = None
        self.id = ""
        self._modifierFound = False
        self.aggregate_previous_rules(parse_list,
                                      ["Star", "Alias", "alias", "IdStartsWithCap", "NamespaceIdentifier",
                                       "NamespaceModifier", "Comma"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "NamespaceModifier":
            self.modifier = parse_info.get_cst()[-1]
            self._modifierFound = True
        elif rule in ["IdStartsWithCap", "NamespaceIdentifier"] and not self._modifierFound:
            self.id = parse_info.id
        elif rule in ["IdStartsWithCap", "NamespaceIdentifier"] and self._modifierFound:
            self.id = parse_info.id
