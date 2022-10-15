"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""


from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTInt import AuxSTInt
from poc.classes.AuxSTVariableVariadic import AuxSTVariableVariadic


class ContextIndexValue(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.predicate = AuxSTVariableVariadic(i)
        self._i = i
        self._sub_index = None
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["IndexValue"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "KeysOfVariadicVariable":
            # register the index
            parsing_info.predicate.register_child(self._sub_index)  # noqa
            for child in reversed(parsing_info.predicate.children):
                child.parent = self.predicate
            self.predicate.id = parsing_info.predicate.id
            # correct the position of the derivation
            self.predicate.zto = self._i.corrected_zpos_by(parsing_info.predicate.zfrom,1) # noqa
            self.predicate.zfrom = parsing_info.predicate.zfrom  # noqa
            self.stop_aggregation = True
        elif rule == "Variable":
            # remember the sub index
            self._sub_index = parsing_info.var  # noqa
        elif rule == "Digit":
            # remember the sub index
            self._sub_index = AuxSTInt(self._i)
            self._sub_index.zto = self._i.last_positions_by_rule['Digit'].pos_to_str()
            self._sub_index.zfrom = self._i.corrected_position('Digit')
            self._sub_index.id = parsing_info.get_cst()

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextIndexValue(i)
        new_info.predicate.zto = i.last_positions_by_rule['IndexValue'].pos_to_str()
        new_info.predicate.children = reversed(new_info.predicate.children)
        i.parse_list.append(new_info)

