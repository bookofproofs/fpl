import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os

"""
Tests of FPL related (transformer) errors.
Note: FPL parser is autogenerated through the TatSu package. Therefore, we do not test any FPL syntax errors.
"""


class FplMisspelledConstructorTests(unittest.TestCase):
    path = None
    util = None
    path_to_grammar = None

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
        "test_FplMisspelledConstructor_first_occurrence.fpl",
        "test_FplMisspelledConstructor_second_occurrence.fpl"
    ])
    def test_errors(self, use_case):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        # exactly one error was found
        self.assertEqual(1, len(interpreter.get_errors()))
        # the error is the same as in the use case file
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))