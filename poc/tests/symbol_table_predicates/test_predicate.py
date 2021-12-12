import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser

"""
Tests of FPL predicate definitions and how they are represented in the symbol table
"""


class AuxPredicateTests(unittest.TestCase):
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
        "test_predicate_01",
        "test_predicate_02",
        "test_predicate_03",
        "test_predicate_04",
        "test_predicate_05",
        "test_predicate_06",
        "test_predicate_07",
        "test_predicate_08",
        "test_predicate_09",
        "test_predicate_10",
        "test_predicate_11",
        "test_predicate_12",
        "test_predicate_13",
        "test_predicate_14",
        "test_predicate_15",
        "test_predicate_16",
    ])
    def test_correct(self, use_case):
        interpreter = FplInterpreter(self.fpl_parser)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(use_case, result[0])
        actual = self.util.remove_object_references_from_string(interpreter.symbol_table_to_str().strip())
        if AuxISourceAnalyser.verbose:
            print(actual)
        self.assertEqual(result[1].strip(), actual)
