import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplsourcetransformer import FPLSourceTransformer

"""
Test if a syntactically correct theory can be prettified and 
and will produce the same minified representation of itself
"""


class PrettifyTestCase(unittest.TestCase):
    maxDiff = None
    fpl_parser = None
    util = None
    transformer = None

    @classmethod
    def setUpClass(cls):
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser("../../grammar/fpl_tatsu_format.ebnf")
        cls.transformer = FPLSourceTransformer(cls.fpl_parser)

    @parameterized.expand([
        "../theories/Commons.fpl",
        "../theories/ArithmeticsNat.fpl",
        "../theories/Set.fpl",
        "../theories/CommonsStructures.fpl",
        "../theories/Algebra.fpl",
        "../theories/Geometry.fpl",
        "../theories/Linalg.fpl",
        "../theories/Example4-7.fpl",
    ])
    def test_cases(self, use_case):
        self.transformer.clear()
        self.transformer.syntax_transform(use_case)
