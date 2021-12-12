import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter

"""
Test if a syntactically correct theory can be prettified and 
and will produce the same minified representation of itself
"""


class PrettifyTestCase(unittest.TestCase):
    util = None
    fpl_parser = None
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser("../../grammar/fpl_tatsu_format.ebnf")
        cls.interpreter = FplInterpreter(cls.fpl_parser)

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
        source = self.util.get_file_content(use_case)
        self.interpreter.syntax_analysis("test_theory", source)
