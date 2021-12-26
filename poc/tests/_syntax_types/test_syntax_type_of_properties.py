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
        "test_syntax_type_of_properties",
    ])
    def test_parser(self, use_case):
        self.transformer.clear()
        self.transformer.syntax_transform(self.path_to_usecases + "/" + use_case + ".fpl")

    @parameterized.expand([
        "test_syntax_type_of_properties_fail_001",
        "test_syntax_type_of_properties_fail_002",
        "test_syntax_type_of_properties_fail_003",
        "test_syntax_type_of_properties_fail_004",
        "test_syntax_type_of_properties_fail_005",
        "test_syntax_type_of_properties_fail_006",
        "test_syntax_type_of_properties_fail_007",
        "test_syntax_type_of_properties_fail_008",
        "test_syntax_type_of_properties_fail_009",
        "test_syntax_type_of_properties_fail_010",
        "test_syntax_type_of_properties_fail_011",
        "test_syntax_type_of_properties_fail_012",
        "test_syntax_type_of_properties_fail_013",
        "test_syntax_type_of_properties_fail_014",
        "test_syntax_type_of_properties_fail_015",
        "test_syntax_type_of_properties_fail_016",
    ])
    def test_fail_parser_property_type(self, use_case):
        # the above tests should fail syntactically,
        # because the they contain a property type that cannot be disambiguated with its signature
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

