"""
This file was generated by the tool TatSuSAG (the TatSu syntax analyser generator)
Changes to this file may cause incorrect behavior and will be lost if the code is regenerated.
"""

from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxRuleDependencies import AuxRuleDependencies
from poc.classes.AuxSymbolTable import AuxSymbolTable


class ContextNamespace(AuxInterpretation):
    def __init__(self, i: AuxISourceAnalyser):
        super().__init__(i.ast_info, i.errors)
        self.extension = None
        self.used_namespaces = None
        self.rules_of_inference = None
        self.building_blocks = None
        self.localisations = None
        # because this is the root rule of the FPL grammar, we have to aggregate all previous rules from the
        # parsing list using (list(AuxRuleDependencies.dep.keys())
        # even if (due to problems in the syntax analysis), the parsing list is not matching the children of the
        # Namespace rule.
        self.aggregate_previous_rules(i.parse_list,
                                      list(AuxRuleDependencies.dep.keys()), self.rule_aggregator)

    def rule_aggregator(self, rule: str, parsing_info: AuxInterpretation):
        if rule == "NamespaceIdentifier":
            self.id = parsing_info.id
            self.stop_aggregation = True
        elif rule == "ExtensionBlock":
            self.extension = parsing_info.extension  # noqa
        elif rule == "UsesClause":
            self.used_namespaces = parsing_info.used_namespaces  # noqa
        elif rule == "RulesOfInferenceBlock":
            self.rules_of_inference = parsing_info.rules_of_inference  # noqa
        elif rule == "TheoryBlock":
            self.building_blocks = parsing_info.building_blocks  # noqa
        elif rule == "LocalizationBlock":
            self.localisations = parsing_info.localizations  # noqa

    @staticmethod
    def dispatch(i: AuxISourceAnalyser, parsing_info: AuxInterpretation):
        new_info = ContextNamespace(i)
        i.theory_node.namespace = new_info.id
        i.parse_list.append(new_info)
