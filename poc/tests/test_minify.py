import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplsourcetransformer import FPLSourceTransformer

"""
Test if a syntactically correct theory can be minified
and will produce the same minified representation of itself
"""


class MinifyTestCase(unittest.TestCase):
    maxDiff = None
    util = None
    fpl_parser = None
    transformer = None

    @classmethod
    def setUpClass(cls):
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser("../../grammar/fpl_tatsu_format.ebnf")
        cls.transformer = FPLSourceTransformer(cls.fpl_parser)
        cls.transformer_after_minify = FPLSourceTransformer(cls.fpl_parser)

    def minify(self, source_path):
        self.transformer.clear()
        self.transformer_after_minify.clear()
        self.transformer.syntax_transform(source_path)
        self.transformer_after_minify.syntax_transform_from_source(self.transformer.get_minified())

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
    @unittest.skip("Skipping tests for performance reasons, comment this line out to include this test.")
    def test_cases(self, use_case):
        self.minify(use_case)
        self.assertEqual(self.transformer.get_minified(), self.transformer_after_minify.get_minified())

