import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplsourcetransformer import FPLSourceTransformer
from tatsu.exceptions import FailedToken
from tatsu.exceptions import FailedParse
from tatsu.exceptions import FailedPattern
import os

"""
Tests of FPL related (parser) errors.
Note: FPL parser is autogenerated through the TatSu package. Therefore, we do not test any FPL syntax errors.
However, we make a positive test to ensure that all that is allowed by the FPL syntax definition can be parsed without
errors. 
"""


class FplSyntaxTests(unittest.TestCase):
    path = None
    path_to_grammar = None
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
        cls.transformer = FPLSourceTransformer(cls.fpl_parser)

    @parameterized.expand([
        "test_syntax_type_calls_ok_01",
        "test_syntax_type_calls_ok_02",
        "test_syntax_type_calls_ok_03",
        "test_syntax_type_calls_ok_04",
        "test_syntax_type_calls_ok_05",
    ])
    def test_parser(self, use_case):
        self.transformer.clear()
        self.transformer.syntax_transform(self.path_to_usecases + "/" + use_case + ".fpl")

    @parameterized.expand([
        "test_syntax_type_calls_fail_01",
        "test_syntax_type_calls_fail_02",
        "test_syntax_type_calls_fail_03",
        "test_syntax_type_calls_fail_04",
        "test_syntax_type_calls_fail_05",
        "test_syntax_type_calls_fail_06",
        "test_syntax_type_calls_fail_07",
        "test_syntax_type_calls_fail_08",
        "test_syntax_type_calls_fail_09",
        "test_syntax_type_calls_fail_10",
        "test_syntax_type_calls_fail_11",
        "test_syntax_type_calls_fail_12",
        "test_syntax_type_calls_fail_13",
        "test_syntax_type_calls_fail_14",
        "test_syntax_type_calls_fail_15",
        "test_syntax_type_calls_fail_16",
        "test_syntax_type_calls_fail_17",
        "test_syntax_type_calls_fail_18",
        "test_syntax_type_calls_fail_19",
        "test_syntax_type_calls_fail_20",
        "test_syntax_type_calls_fail_21",
        "test_syntax_type_calls_fail_22",
        "test_syntax_type_calls_fail_23",
        "test_syntax_type_calls_fail_24",
    ])
    def test_fail_parser_calls(self, use_case):
        # the above tests should fail syntactically,
        # because the they contain a "call" using anonymous types instead of variables
        try:
            self.transformer.clear()
            self.transformer.syntax_transform(self.path_to_usecases + "/" + use_case + ".fpl")
        except FailedToken as ex:
            return
        except FailedParse as ex:
            return
        except FailedPattern as ex:
            return
        self.assertFalse(True)

    @parameterized.expand([
        "test_syntax_type_var_declarations_in_block_fail_01",
        "test_syntax_type_var_declarations_in_block_fail_02",
        "test_syntax_type_var_declarations_in_block_fail_03",
        "test_syntax_type_var_declarations_in_block_fail_04",
        "test_syntax_type_var_declarations_in_block_fail_05",
        "test_syntax_type_var_declarations_in_block_fail_06",
        "test_syntax_type_var_declarations_in_block_fail_07",
        "test_syntax_type_var_declarations_in_block_fail_08",
    ])
    def test_fail_parser_signature(self, use_case):
        # the above tests should fail syntactically,
        # because the they contain a signature containing some anonymous types instead of declared variables
        try:
            self.transformer.clear()
            self.transformer.syntax_transform(self.path_to_usecases + "/" + use_case + ".fpl")
        except FailedToken as ex:
            return
        except FailedParse as ex:
            return
        except FailedPattern as ex:
            return
        self.assertFalse(True)
