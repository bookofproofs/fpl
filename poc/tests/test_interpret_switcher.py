import unittest
from ..classes.AuxAggrRulesText import aggr_rules_text
from ..fplsemantics import FPLSemantics

"""
Test if the interpretation switcher in semantics selects the correct interpretation function.
For instance, all functions 'inter_equals_proceeding_ignored_rules' in switcher must be in 
IgnoreRules.ignorable_rules and vice versa. Otherwise the interpreter might not work correctly.
"""


class ConsistentSwitcher(unittest.TestCase):

    def test_switcher_selects_correct_function(self):
        self.semantics = FPLSemantics()
        for sw in self.semantics.switcher:
            rule = self.semantics.switcher.get(sw)
            if rule.__name__ == "inter_equals_proceeding_ignored_rules":
                self.assertIn(sw, aggr_rules_text)

    def test_all_ignorable_rules_have_in_switcher_correct_function(self):
        self.semantics = FPLSemantics()
        for sw in aggr_rules_text:
            rule = self.semantics.switcher.get(sw, lambda: "Invalid rule")
            if rule.__name__ == "Invalid rule":
                raise NameError("Invalid rule " + sw + " in ignorable_rules")
            self.assertEqual(sw + ":" + "inter_equals_proceeding_ignored_rules", sw + ":" + rule.__name__)
