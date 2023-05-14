"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSTVarSpecList import AuxSTVarSpecList
from poc.classes.AuxSTProperties import AuxSTProperties
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.ContextVariableSpecificationList import ContextVariableSpecificationList


class ContextPredicateDefinitionBlock(AuxInterpretation):

    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self._i = i
        # Predicate is optional in the grammar, and we initialize it in any case
        self.predicate = AuxSTPredicate(AuxSTConstants.intrinsic, i)
        # specification list is optional in the grammar, and we initialize it in any case
        self.variable_spec = AuxSTVarSpecList()
        # definition content list is optional in the grammar, and we initialize it in any case
        self.property_list = AuxSTProperties()
        self.aggregate_previous_rules(i.parse_list,
                                      AuxRuleDependencies.dep["PredicateDefinitionBlock"] +
                                      AuxRuleDependencies.dep["PropertyList"] +
                                      ["VariableSpecification"], self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "LeftBrace":
            self.stop_aggregation = True
        elif rule == "Predicate":
            if parsing_info.predicate is not None:
                self.predicate = parsing_info.predicate  # noqa
        elif rule == "VariableSpecification":
            ContextVariableSpecificationList.consume_variable_specification(self._i, parsing_info, self)
        elif rule == "VariableSpecificationList":
            self.variable_spec = parsing_info.variable_spec  # noqa
        elif rule == "Property":
            parsing_info.building_block.parent = self.property_list  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextPredicateDefinitionBlock(i)
        new_info.property_list.children = reversed(new_info.property_list.children)
        i.parse_list.append(new_info)
