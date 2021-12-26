from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSTUsedTheory import AuxSTUsedTheory


class ContextWildcardTheoryNamespace(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.used_namespace = AuxSTUsedTheory(i)
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      ["Star", "Alias", "alias", "IdStartsWithCap", "NamespaceIdentifier",
                                       "NamespaceModifier", "Comma"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parse_info: AuxInterpretation):
        if rule == "NamespaceModifier":
            self.used_namespace.modifier = parse_info.get_cst()[-1]
            if self.used_namespace.modifier == "*":
                self.used_namespace.zfrom = self._i.corrected_position_by("NamespaceIdentifier", -2)
        elif rule in ["IdStartsWithCap", "NamespaceIdentifier"]:
            self.used_namespace.id = parse_info.id
            self.used_namespace.zfrom = self._i.corrected_position_by(rule, len(parse_info.id))

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextWildcardTheoryNamespace(i)
        i.parse_list.append(new_info)
