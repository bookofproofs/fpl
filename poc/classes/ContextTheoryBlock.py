from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextTheoryBlock(AuxInterpretation):
    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.building_blocks = []
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["TheoryBlock"] +
                                      AuxRuleDependencies.dep["BuildingBlockList"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "TheoryHeader":
            self.stop_aggregation = True
        elif rule == "BuildingBlock":
            self.building_blocks.append(parsing_info.building_block)  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextTheoryBlock(i.parse_list, parsing_info)
        for block in reversed(new_info.building_blocks):
            if block.outline == AuxSymbolTable.block_def and block.def_type == AuxSymbolTable.classDeclaration:
                AuxSymbolTable.add_class_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_axiom:
                AuxSymbolTable.add_axiom_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_def and block.def_type == AuxSymbolTable.predicateDeclaration:
                AuxSymbolTable.add_predicate_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_def and block.def_type == AuxSymbolTable.functionalTerm:
                AuxSymbolTable.add_functional_term_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_thm:
                AuxSymbolTable.add_theorem_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_lem:
                AuxSymbolTable.add_lemma_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_prop:
                AuxSymbolTable.add_proposition_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_conj:
                AuxSymbolTable.add_conjecture_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_cor:
                AuxSymbolTable.add_corollary_to_theory(i.theory_node, block)
            elif block.outline == AuxSymbolTable.block_proof:
                AuxSymbolTable.add_proof_to_theory(i.theory_node, block)
            else:
                raise NotImplementedError(block.outline)
        i.parse_list.append(new_info)
