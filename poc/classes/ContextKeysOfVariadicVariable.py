"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTPredicate import AuxSTPredicate


class ContextKeysOfVariadicVariable(AuxInterpretation):

    def __init__(self, parse_list: list, parsing_info: AuxInterpretation):
        super().__init__(parsing_info.get_ast_info(), parsing_info.get_errors())
        self.predicate = AuxSTPredicate(AuxSymbolTable.variadic_var, parsing_info)
        self.aggregate_previous_rules(parse_list,
                                      AuxRuleDependencies.dep["KeysOfVariadicVariable"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "Variable":
            self.predicate.register_child(parsing_info.var)  # noqa
            self.stop_aggregation = True

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextKeysOfVariadicVariable(i.parse_list, parsing_info)
        i.parse_list.append(new_info)
