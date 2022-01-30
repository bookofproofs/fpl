"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTPredicate import AuxSTPredicate


class ContextIndexValue(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTPredicate(AuxSymbolTable.index_value, i)
        self._i = i
        self._sub_index = None
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["IndexValue"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "KeysOfVariadicVariable":
            # register the index
            parsing_info.predicate.register_child(self._sub_index)  # noqa
            self.predicate.register_child(parsing_info.predicate)  # noqa
            self.predicate.set_id(parsing_info.predicate.id + self._sub_index.id)
            # correct the starting position of the derivation
            self.predicate.zfrom = parsing_info.predicate.zfrom  # noqa
            self.stop_aggregation = True
        elif rule == "Variable":
            # remember the sub index
            self._sub_index = parsing_info.var  # noqa
        elif rule == "Digit":
            # remember the sub index
            self._sub_index = AuxSTPredicate(AuxSymbolTable.digit, self._i)
            self._sub_index.set_id(parsing_info.get_cst())

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextIndexValue(i)
        new_info.predicate.children = reversed(new_info.predicate.children)
        i.parse_list.append(new_info)

