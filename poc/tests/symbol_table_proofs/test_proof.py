import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser

"""
Tests of FPL predicate definitions and how they are represented in the symbol table
"""


class ProofsTests(unittest.TestCase):
    path = None
    util = None
    path_to_grammar = None
    maxDiff = None
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
        "test_proof_01.fpl",
        "test_proof_02.fpl",
        "test_proof_03.fpl",
        "test_proof_04.fpl",
    ])
    def test_correct(self, use_case):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        actual = self.util.adjust_symbol_table_for_testing(interpreter)
        if AuxISourceAnalyser.verbose:
            print(actual)
            if ProofsTests.rewrite and result[1].strip() != actual:
                self.util.rewrite_expected_test_case(self.path_to_usecases, use_case, actual)
        else:
            if ProofsTests.rewrite:
                self.assertEqual(ProofsTests.rewrite,
                                 "Please set rewrite flag to false unless you really want override the expected values")
        self.assertEqual(result[1].strip(), actual)
