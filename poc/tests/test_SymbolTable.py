import unittest
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import poc.fplerror
import os
import re

"""
Tests if the interpreter produces the expected symbol tables for different syntactically correct fpl files.
These files have two sections each separated by at least 30*'#', followed by a string representation of the 
resulting symbol table 
"""


class SymbolTableTests(unittest.TestCase):
    util = None
    fpl_parser = None
    maxDiff = None
    path_to_grammar = None
    path_to_usecases = None

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.normpath(os.path.abspath(__file__))
        if os.path.isfile(cls.path):
            cls.path = os.path.dirname(cls.path)
        cls.path_to_grammar = os.path.join(cls.path, "../../grammar")
        cls.path_to_usecases = os.path.join(cls.path, "usecases")
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser(cls.path_to_grammar + "/fpl_tatsu_format.ebnf")

    def get_code_and_expected(self, use_case_name):
        file_content = self.util.get_file_content(self.path_to_usecases + "/" + use_case_name + ".txt")
        return file_content.split('##############################')

    @staticmethod
    def remove_object_references_from_string(test_output: str):
        """
        Removes from the test output all dynamic object memory addresses because they are irrelevant for the test.
        :param test_output: output of the test
        :return: test_result replaced
        """
        test_output = test_output.replace("poc.classes.", "")
        return re.sub(' object at 0x[0-9A-F]+', '', test_output)

    def test_uc_empty(self):
        use_case = "uc_empty"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(), interpreter.symbol_table_to_str())

    def test_uc_namespace(self):
        use_case = "uc_namespace"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_namespace_modified_with_star(self):
        use_case = "uc_namespace_modified_with_star"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_namespace_modified_with_alias(self):
        use_case = "uc_namespace_modified_with_alias"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_namespace_modified_with_diverse(self):
        use_case = "uc_namespace_modified_with_diverse"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_namespace_with_duplicate(self):
        use_case = "uc_namespace_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_inference_rules_one(self):
        use_case = "uc_inference_rules_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_inference_rules_two(self):
        use_case = "uc_inference_rules_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_inference_rules_three_with_duplicate(self):
        use_case = "uc_inference_rules_three_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_class_one(self):
        use_case = "uc_class_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_two(self):
        use_case = "uc_class_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_duplicate(self):
        use_case = "uc_class_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_predicate_declaration_one(self):
        use_case = "uc_predicate_declaration_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_predicate_declaration_two(self):
        use_case = "uc_predicate_declaration_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_predicate_declaration_with_duplicate(self):
        use_case = "uc_predicate_declaration_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_functional_term_one(self):
        use_case = "uc_functional_term_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_functional_term_two(self):
        use_case = "uc_functional_term_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_functional_term_with_duplicate(self):
        use_case = "uc_functional_term_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_axiom_one(self):
        use_case = "uc_axiom_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_axiom_two(self):
        use_case = "uc_axiom_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_axiom_with_duplicate(self):
        use_case = "uc_axiom_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_class_with_constructor_one(self):
        use_case = "uc_class_with_constructor_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_constructor_two(self):
        use_case = "uc_class_with_constructor_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_func_property_one(self):
        use_case = "uc_class_with_func_property_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_func_property_two(self):
        use_case = "uc_class_with_func_property_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_class_instance_property_one(self):
        use_case = "uc_class_with_class_instance_property_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_class_instance_property_two(self):
        use_case = "uc_class_with_class_instance_property_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_class_instance_property_with_duplicate(self):
        use_case = "uc_class_with_class_instance_property_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_class_with_class_instance_template_property_one(self):
        use_case = "uc_class_with_class_instance_template_property_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_class_instance_template_property_two(self):
        use_case = "uc_class_with_class_instance_template_property_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_class_instance_template_property_with_duplicate(self):
        use_case = "uc_class_with_class_instance_template_property_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_class_with_class_with_mixed_properties(self):
        use_case = "uc_class_with_mixed_properties"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_class_with_func_property_with_duplicate(self):
        use_case = "uc_class_with_func_property_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_theorem_one(self):
        use_case = "uc_theorem_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_theorem_two(self):
        use_case = "uc_theorem_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_theorem_with_duplicate(self):
        use_case = "uc_theorem_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_corollary_one(self):
        use_case = "uc_corollary_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_corollary_two(self):
        use_case = "uc_corollary_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_corollary_with_duplicate(self):
        use_case = "uc_corollary_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_proposition_one(self):
        use_case = "uc_proposition_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_proposition_two(self):
        use_case = "uc_proposition_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_proposition_with_duplicate(self):
        use_case = "uc_proposition_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_lemma_one(self):
        use_case = "uc_lemma_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_lemma_two(self):
        use_case = "uc_lemma_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_lemma_with_duplicate(self):
        use_case = "uc_lemma_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_conjecture_one(self):
        use_case = "uc_conjecture_one"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_conjecture_two(self):
        use_case = "uc_conjecture_two"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))

    def test_uc_conjecture_with_duplicate(self):
        use_case = "uc_conjecture_with_duplicate"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEqual(1, len(interpreter.get_errors()))
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))

    def test_uc_anonymous_signature(self):
        use_case = "uc_anonymous_signature"
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        self.assertEquals(result[1].strip(),
                          SymbolTableTests.remove_object_references_from_string(interpreter.symbol_table_to_str()))
