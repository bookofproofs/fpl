from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxHighlightTag import AuxHighlightTag


class ContextPredicateIdentifier(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["PredicateIdentifier"] +
                                      AuxRuleDependencies.dep["AliasedId"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "IdStartsWithCap":
            self.id = parsing_info.get_cst() + self.id
        elif rule == "Dot":
            self.id = parsing_info.get_cst() + self.id

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPredicateIdentifier(i)
        new_info.id = ContextPredicateIdentifier._strip_dots(new_info.id)
        new_info.zfrom.correct_offset(len(new_info.id)+1)
        new_info.zto.correct_offset(1)
        i.highlight_tags.append(AuxHighlightTag("identifier", new_info.zfrom, new_info.zto))
        i.parse_list.append(new_info)

    @staticmethod
    def _strip_dots(identifier: str):
        if identifier[-1] == ".":
            identifier = identifier[0:-1]
        if identifier[0] == ".":
            identifier = identifier[1:]
        return identifier
