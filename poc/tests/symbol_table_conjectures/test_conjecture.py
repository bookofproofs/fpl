import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser

"""
Tests of FPL conjectures and how they are represented in the symbol table
"""


class ConjecturesTests(unittest.TestCase):
    maxDiff = None
    path = None
    path_to_grammar = None
    path_to_usecases = None
    fpl_parser = None
    util = None

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
        "test_conjecture_01",
        "test_conjecture_02",
    ])
    def test_possibilities(self, use_case):
        interpreter = FplInterpreter(self.fpl_parser)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(use_case, result[0])
        actual = self.util.remove_object_references_from_string(interpreter.symbol_table_to_str().strip())
        if AuxISourceAnalyser.verbose:
            print(actual)
        self.assertEqual(result[1].strip(), actual)


