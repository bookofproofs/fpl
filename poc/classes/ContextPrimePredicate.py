from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxSTExt import AuxSTExt
from poc.classes.AuxRuleDependencies import AuxRuleDependencies


class ContextPrimePredicate(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = None
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["PrimePredicate"] + ["Assignee"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        self.id = parsing_info.id
        if rule == "PredicateWithArguments":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "QualifiedIdentifier":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "Statement":
            self.predicate = parsing_info.statement  # noqa
        elif rule == "IndexValue":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "Identifier":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "IsOperator":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "true":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "false":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "UndefinedHeader":
            self.predicate = parsing_info.predicate  # noqa
        elif rule == "ArgumentParam":
            self.predicate = parsing_info.predicate  # noqa
        elif rule.startswith("ext"):
            self.predicate = AuxSTExt(rule, self._i)
            self.predicate.zto = self._i.last_positions_by_rule[rule].pos_to_str()
            self.predicate.zfrom = self._i.corrected_position(rule)
            self.predicate.id = parsing_info.get_cst()
        self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        p_info = ContextPrimePredicate(i)
        i.parse_list.append(p_info)
