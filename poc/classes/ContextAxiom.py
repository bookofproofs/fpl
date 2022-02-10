from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTAxiom import AuxSTAxiom
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextAxiom(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.building_block = AuxSTAxiom(i)
        self._i = i
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["Axiom"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "AxiomHeader":
            self.building_block.keyword = parsing_info.id
            self.stop_aggregation = True
        elif rule == "Signature":
            self.building_block.register_child(parsing_info.symbol_signature)  # noqa
            self.building_block.id = parsing_info.symbol_signature.to_string()  # noqa
        elif rule == "AxiomBlock":
            if parsing_info.predicate is None:
                self.building_block.register_child(AuxSTPredicate(AuxSymbolTable.intrinsic, self._i))
            else:
                self.building_block.register_child(parsing_info.predicate)  # noqa
            self.building_block.register_child(parsing_info.variable_spec)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextAxiom(i)
        new_info.building_block.children = reversed(new_info.building_block.children)
        i.parse_list.append(new_info)
