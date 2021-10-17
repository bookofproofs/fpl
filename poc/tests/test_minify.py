import unittest
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
        self.interpreter_after_minify.syntax_transform("minified_test_theory_name", self.interpreter.minified())
        if self.interpreter_after_minify.has_errors():
            self.interpreter_after_minify.print_errors()

    def test_minify_common(self):
        self.minify("../theories/Commons.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    def test_minify_ArithmeticsNat(self):
        self.minify("../theories/ArithmeticsNat.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Set(self):
        self.minify("../theories/Set.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_CommonStructures(self):
        self.minify("../theories/CommonsStructures.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Algebra(self):
        self.minify("../theories/Algebra.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Geometry(self):
        self.minify("../theories/Geometry.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_Linalg(self):
        self.minify("../theories/Linalg.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())

    # test case minification
    def test_minify_example25(self):
        self.minify("../theories/Example4-7.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_minify.has_errors())
        self.assertEqual(self.interpreter.minified(), self.interpreter_after_minify.minified())


if __name__ == '__main__':
    unittest.main()
