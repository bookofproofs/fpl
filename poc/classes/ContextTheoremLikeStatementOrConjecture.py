from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTTheorem import AuxSTTheorem
from poc.classes.AuxSTProposition import AuxSTProposition
from poc.classes.AuxSTCorollary import AuxSTCorollary
from poc.classes.AuxSTLemma import AuxSTLemma
from poc.classes.AuxSTConjecture import AuxSTConjecture


class ContextTheoremLikeStatementOrConjecture(AuxInterpretation):
    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self._signature = None
        self.building_block = None
        self._premise_conclusion_block = None
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["TheoremLikeStatementOrConjecture"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "TheoremLikeStatementOrConjectureHeader":
            if parsing_info.id in ["theorem", "thm"]:
                self.building_block = AuxSTTheorem(parsing_info)
            elif parsing_info.id in ["lemma", "lem"]:
                self.building_block = AuxSTLemma(parsing_info)
            elif parsing_info.id in ["proposition", "prop"]:
                self.building_block = AuxSTProposition(parsing_info)
            elif parsing_info.id in ["corollary", "cor"]:
                self.building_block = AuxSTCorollary(parsing_info)
            elif parsing_info.id in ["conjecture", "conj"]:
                self.building_block = AuxSTConjecture(parsing_info)
            else:
                raise NotImplementedError(parsing_info.id)
            self.building_block.register_child(self._signature)
            self.building_block.id = self._signature.to_string()
            self.building_block.register_child(self._premise_conclusion_block.variable_spec)
            self.building_block.register_child(self._premise_conclusion_block.pre)
            self.building_block.register_child(self._premise_conclusion_block.con)
        elif rule == "Signature":
            self._signature = parsing_info.symbol_signature  # noqa
        elif rule == "CorollarySignature":
            self._signature = parsing_info.symbol_signature  # noqa
        elif rule == "PremiseConclusionBlock":
            self._premise_conclusion_block = parsing_info

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextTheoremLikeStatementOrConjecture(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
