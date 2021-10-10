import unittest
from classes.AuxStringConcatenationRules import aggr_rules_text
from fplsourceanalyser import FPLSourceAnalyser
from anytree import AnyNode

"""
Test if the interpretation switcher in semantics selects the correct interpretation function.
For instance, all functions 'concatenation_of_proceeding_string_rules' in switcher must be in 
IgnoreRules.ignorable_rules and vice versa. Otherwise the interpreter might not work correctly.
"""


class ConsistentSwitcher(unittest.TestCase):

    def test_switcher_selects_correct_function(self):
        root = AnyNode()
        self.semantics = FPLSourceAnalyser(root, "test", [])
        for sw in self.semantics.switcher:
            rule = self.semantics.switcher.get(sw)
            if rule.__name__ == "concatenation_of_proceeding_string_rules":
                self.assertIn(sw, aggr_rules_text)

    def test_all_string_concat_rules_have_in_switcher_correct_function(self):
        root = AnyNode()
        self.semantics = FPLSourceAnalyser(root, "test", [])
        for key in aggr_rules_text:
            rule_delegate = self.semantics.switcher.get(key, lambda: "Dummy")
            if rule_delegate.__name__ == "Dummy":
                raise NameError("Unrecognized rule " + key + " in aggr_rules_text")
            # some_additional_action contains those rules in aggr_rules_text that need some additional action
            # (like for instance changing the parsing context for the interpretations being still ahead).
            # The switcher will call other delegates instead of 'concatenation_of_proceeding_string_rules'
            # in which 'concatenation_of_proceeding_string_rules' is usually called as a first step,
            # followed by some additional action.
            # Therefore, some_other_action extends this test by some special cases, while
            # key + ":" + "concatenation_of_proceeding_string_rules" is the asserted default case.
            some_additional_action = \
                ["NamespaceIdentifier:namespace_identifier_dispatcher",
                 "PredicateIdentifier:predicate_identifier_dispatcher"
                 ]
            self.assertIn(key + ":" + rule_delegate.__name__,
                          some_additional_action +
                          [key + ":" + "concatenation_of_proceeding_string_rules"])

    def test_all_string_concat_aggregated_rules_have_in_switcher_correct_function(self):
        root = AnyNode()
        self.semantics = FPLSourceAnalyser(root, "test", [])
        for key in aggr_rules_text:
            rule = self.semantics.switcher.get(key, lambda: "Dummy")
            if rule.__name__ == "Dummy":
                raise NameError("Unrecognized rule " + key + " in ignorable_rules")
            for aggregated_rule in aggr_rules_text[key]:
                rule_delegate = self.semantics.switcher.get(aggregated_rule, lambda: "Dummy")
                # the to-be aggregated production must have a string_interpretation or an aggregation
                # of such productions
                self.assertIn(aggregated_rule + ":" + rule_delegate.__name__,
                              [aggregated_rule + ":" + "string_interpretation",
                               aggregated_rule + ":" + "concatenation_of_proceeding_string_rules"])

