"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTConstructors import AuxSTConstructors
from poc.classes.AuxSTProperties import AuxSTProperties


class ContextObjectDefinitionBlock(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        # specification list is optional in the grammar and we initialize it in any case
        self.variable_spec = AuxSTVarSpecList()
        # definition content lists (properties and/or constructors) are optional in the grammar
        # and we initialize them in any case
        self.constructor_list = AuxSTConstructors()
        self.property_list = AuxSTProperties()
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["ObjectDefinitionBlock"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "LeftBrace":
            self.stop_aggregation = True
        elif rule == "VariableSpecificationList":
            self.variable_spec = parsing_info.variable_spec  # noqa
        elif rule == "DefinitionContentList":
            self.constructor_list = parsing_info.constructor_list  # noqa
            self.property_list = parsing_info.property_list  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextObjectDefinitionBlock(i)
        i.parse_list.append(new_info)