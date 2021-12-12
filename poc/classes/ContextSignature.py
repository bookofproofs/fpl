from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTSignature import AuxSTSignature


class ContextSignature(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.symbol_signature = AuxSTSignature(parsing_info)
        self.aggregate_previous_rules(parse_list, AuxRuleDependencies.dep["Signature"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PredicateIdentifier":
            self.symbol_signature.set_id(parsing_info.id)
            self.stop_aggregation = True
        elif rule == "ParamTuple":
            self.symbol_signature.set_params(parsing_info.tuple)

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextSignature(i.parse_list, parsing_info)
        new_info.symbol_signature.make()
        i.parse_list.append(new_info)
