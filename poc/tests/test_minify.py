import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter

"""
Test if a syntactically correct theory can be minified
and will produce the same minified representation of itself
"""


class MinifyTestCase(unittest.TestCase):
    util = None
    fpl_parser = None
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser("../../grammar/fpl_tatsu_format.ebnf")
        cls.interpreter = FplInterpreter(cls.fpl_parser)
        cls.interpreter_after_minify = FplInterpreter(cls.fpl_parser)

    def minify(self, source_path):
        theory_source = self.util.get_file_content(source_path)
        self.interpreter.clear()
        self.interpreter_after_minify.get_errors().clear()

        self.interpreter.syntax_transform("test_theory_name", theory_source)
        self.interpreter_after_minify.syntax_transform("minified_test_theory_name",
                                                       self.interpreter.minified("test_theory_name"))
        if self.interpreter_after_minify.has_errors():
            self.interpreter_after_minify.print_errors()

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
        self.minify(use_case)
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified("test_theory_name"),
                         self.interpreter_after_minify.minified("minified_test_theory_name"))

