import unittest
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
        cls.interpreter_after_prettify = FplInterpreter(cls.fpl_parser)

    def prettify(self, source_path):
        theory_source = self.util.get_file_content(source_path)
        self.interpreter.clear()
        self.interpreter_after_prettify.clear()

        self.interpreter.syntax_transform("test_theory_name", theory_source)
        self.interpreter_after_prettify.syntax_transform("prettified_test_theory_name", self.interpreter.prettyfied())
        if self.interpreter_after_prettify.has_errors():
            self.interpreter_after_prettify.print_errors()

    def test_prettify_common(self):
        self.prettify("../theories/Commons.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    def test_prettify_ArithmeticsNat(self):
        self.prettify("../theories/ArithmeticsNat.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Set(self):
        self.prettify("../theories/Set.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_CommonStructures(self):
        self.prettify("../theories/CommonsStructures.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Algebra(self):
        self.prettify("../theories/Algebra.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Geometry(self):
        self.prettify("../theories/Geometry.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Linalg(self):
        self.prettify("../theories/Linalg.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_example25(self):
        self.prettify("../theories/Example4-7.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())


if __name__ == '__main__':
    unittest.main()
