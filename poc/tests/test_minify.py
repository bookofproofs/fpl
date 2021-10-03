import unittest
from ..util.fplutil import Utils
from ..fplinterpreter import FplInterpreter

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

    def interpret(self, source_path):
        theory_source = self.util.get_file_content(source_path)
        self.interpreter.get_errors().clear()
        self.interpreter.symbol_table_clear()
        self.interpreter_after_minify.get_errors().clear()

        self.interpreter.syntax_analysis("test_theory_name", theory_source)
        self.interpreter_after_minify.syntax_analysis("minified_test_theory_name", self.interpreter.minified())
        if self.interpreter_after_minify.has_errors():
            self.interpreter_after_minify.print_errors()

    def test_minify_common(self):
        self.interpret("../theories/Commons.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    def test_minify_ArithmeticsNat(self):
        self.interpret("../theories/ArithmeticsNat.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Set(self):
        self.interpret("../theories/Set.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_CommonStructures(self):
        self.interpret("../theories/CommonsStructures.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Algebra(self):
        self.interpret("../theories/Algebra.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Geometry(self):
        self.interpret("../theories/Geometry.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Linalg(self):
        self.interpret("../theories/Linalg.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_example25(self):
        self.interpret("../theories/Example4-7.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())


if __name__ == '__main__':
    unittest.main()
