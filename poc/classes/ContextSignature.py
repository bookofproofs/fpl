from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTSignature import AuxSTSignature


class ContextSignature(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.symbol_signature = AuxSTSignature(i)
        self._i = i
        self.aggregate_previous_rules(i.parse_list, AuxRuleDependencies.dep["Signature"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "PredicateIdentifier":
            self.symbol_signature.set_id(parsing_info.id)
            self.symbol_signature.zfrom = str(parsing_info.zfrom)
            self.stop_aggregation = True
        elif rule == "ParamTuple":
            self.symbol_signature.set_params(parsing_info.tuple)
            # because the signature might contain other PredicateIdentifiers in the ParamTuple,
            # we have to correct the beginning of the signature by the beginning of the ParamTuple
            self.symbol_signature.zfrom = parsing_info.zfrom  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextSignature(i)
        new_info.symbol_signature.make()
        i.parse_list.append(new_info)
