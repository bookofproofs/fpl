import unittest
from poc.classes.AuxSymbolTable import AuxSymbolTable
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class RobustnessTests(unittest.TestCase):
    path = None
    util = None
    path_to_grammar = None
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.normpath(os.path.abspath(__file__))
        if os.path.isfile(cls.path):
            cls.path = os.path.dirname(cls.path)
        cls.path_to_grammar = os.path.join(cls.path, "../../../grammar")
        cls.path_to_usecases = os.path.join(cls.path)
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser(cls.path_to_grammar + "/fpl_tatsu_format.ebnf")

    @parameterized.expand([
        ("test_robustness_isOperator.fpl", 299),
        ("test_robustness_predicate.fpl", 556),
        ("test_robustness_types_image.fpl", 309),
        ("test_robustness_types_class.fpl", 192),
        ("test_robustness_types_var_decl.fpl", 1),
        ("test_robustness_types_var_in_signature.fpl", 309),
        ("test_robustness_types_properties.fpl", 315),
    ])
    def test_correct(self, use_case, number_of_nodes):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        r = interpreter.get_symbol_table_root()
        globals_node = AuxSymbolTable.get_child_by_outline(r, AuxSymbolTable.globals)
        self.assertEqual(number_of_nodes, len(globals_node.children))
