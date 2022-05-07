import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser

"""
Tests of FPL theorems and how they are represented in the symbol table
"""


class TheoremsTests(unittest.TestCase):
    maxDiff = None
    path = None
    path_to_grammar = None
    path_to_usecases = None
    fpl_parser = None
    util = None
    rewrite = False

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
        "test_theorem_01.fpl",
        "test_theorem_02.fpl",
    ])
    def test_possibilities(self, use_case):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        actual = self.util.adjust_symbol_table_for_testing(interpreter)
        if AuxISourceAnalyser.verbose:
            print(actual)
            if TheoremsTests.rewrite and result[1].strip() != actual:
                self.util.rewrite_expected_test_case(self.path_to_usecases, use_case, actual)
        else:
            if TheoremsTests.rewrite:
                self.assertEqual(TheoremsTests.rewrite,
                                 "Please set rewrite flag to false unless you really want override the expected values")
        self.assertEqual(result[1].strip(), actual)
