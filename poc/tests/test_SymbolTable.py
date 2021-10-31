import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os
import re

"""
Tests if the interpreter produces the expected symbol tables for different syntactically correct fpl files.
These files have two sections each separated by at least 30*'#', followed by a string representation of the 
resulting symbol table 
"""


class SymbolTableTests(unittest.TestCase):
    path = None
    util = None
    path_to_grammar = None
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.normpath(os.path.abspath(__file__))
        if os.path.isfile(cls.path):
            cls.path = os.path.dirname(cls.path)
        cls.path_to_grammar = os.path.join(cls.path, "../../grammar")
        cls.path_to_usecases = os.path.join(cls.path, "usecases")
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser(cls.path_to_grammar + "/fpl_tatsu_format.ebnf")

    @parameterized.expand([
        "uc_anonymous_signature",
        "uc_axiom_one",
        "uc_axiom_two",
        "uc_empty",
        "uc_namespace",
        "uc_namespace_modified_with_star",
        "uc_namespace_modified_with_alias",
        "uc_namespace_modified_with_diverse",
        "uc_inference_rules_one",
        "uc_inference_rules_two",
        "uc_class_one",
        "uc_class_two",
        "uc_predicate_declaration_one",
        "uc_predicate_declaration_two",
        "uc_functional_term_one",
        "uc_functional_term_two",
        "uc_class_with_constructor_one",
        "uc_class_with_constructor_two",
        "uc_class_with_func_property_one",
        "uc_class_with_func_property_two",
        "uc_class_with_class_instance_property_one",
        "uc_class_with_class_instance_property_two",
        "uc_functional_term_with_property_one",
        "uc_functional_term_with_property_two",
        "uc_class_with_mixed_properties",
        "uc_theorem_one",
        "uc_theorem_two",
        "uc_corollary_one",
        "uc_corollary_two",
        "uc_proposition_one",
        "uc_proposition_two",
        "uc_lemma_one",
        "uc_lemma_two",
        "uc_conjecture_one",
        "uc_conjecture_two",
    ])
    def test_symbol_table_correct(self, use_case):
        interpreter = FplInterpreter(self.fpl_parser)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(use_case, result[0])
        actual = self.util.remove_object_references_from_string(interpreter.symbol_table_to_str().strip())
        print(actual)
        self.assertEqual(result[1].strip(), actual)
