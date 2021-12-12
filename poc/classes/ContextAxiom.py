from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTAxiom import AuxSTAxiom


class ContextAxiom(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.building_block = AuxSTAxiom(parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["Axiom"] + AuxRuleDependencies.dep["AxiomHeader"],
                                      self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule in AuxRuleDependencies.dep["AxiomHeader"]:
            self.stop_aggregation = True
        elif rule == "Signature":
            parsing_info.symbol_signature.make()
            self.building_block.register_child(parsing_info.symbol_signature)
            self.building_block.id = parsing_info.symbol_signature.to_string()
        elif rule == "AxiomBlock":
            self.building_block.register_child(parsing_info.predicate)
            self.building_block.register_child(parsing_info.variable_spec)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextAxiom(i.parse_list, parsing_info)
        new_info.building_block.children = reversed(new_info.building_block.children)
        i.parse_list.append(new_info)

    """
    @staticmethod
    def start(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        i.context.push_context(AuxContext.axiom, i.get_debug_parsing_info(parsing_info))
        ContextSignature.start(i, parsing_info)

    @staticmethod
    def stop(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        axiom_info = Axiom(i.parse_list, parsing_info)
        i.context.pop_context([AuxContext.axiom], i.get_debug_parsing_info(parsing_info))
        i.pop_node()  # forget the axiom node
        i.parse_list.append(axiom_info)
    """