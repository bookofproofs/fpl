import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os

"""
Tests of FPL related (interpreter) errors.
Note: FPL parser is autogenerated through the TatSu package. Therefore, we do not test any FPL syntax errors.
"""


class FplVariableDuplicateInVariableListTests(unittest.TestCase):
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

    def get_code_and_expected(self, use_case_name):
        file_content = self.util.get_file_content(self.path_to_usecases + "/" + use_case_name + ".txt")
        return file_content.split('##############################')

    @parameterized.expand([
        "test_FplVariableDuplicateInVariableList_constructor_signature",
        "test_FplVariableDuplicateInVariableList_other_signature",
        "test_FplVariableDuplicateInVariableList_var_declaration",
    ])
    def test_errors(self, use_case):
        interpreter = FplInterpreter(self.fpl_parser)
        result = self.get_code_and_expected(use_case)
        interpreter.syntax_analysis(use_case, result[0])
        # exactly one error was found
        self.assertEqual(1, len(interpreter.get_errors()))
        # the error is the same as in the use case file
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))
