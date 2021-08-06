import unittest
from ..util.fplutil import Utils
from ..fplinterpreter import FplInterpreter

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

    def interpret(self, source_path):
        self.theory_source = self.util.get_file_content(source_path)
        self.interpreter = FplInterpreter("test_theory", self.theory_source, self.fpl_parser)
        self.interpreter_after_prettify = FplInterpreter("test_theory", self.interpreter.prettyfied(), self.fpl_parser)
        if self.interpreter_after_prettify.has_errors():
            self.interpreter_after_prettify.print_errors()

    def test_prettify_common(self):
        self.interpret("../theories/Commons.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    def test_prettify_ArithmeticsNat(self):
        self.interpret("../theories/ArithmeticsNat.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Set(self):
        self.interpret("../theories/Set.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_CommonStructures(self):
        self.interpret("../theories/CommonsStructures.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Algebra(self):
        self.interpret("../theories/Algebra.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Geometry(self):
        self.interpret("../theories/Geometry.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_Linalg(self):
        self.interpret("../theories/Linalg.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())

    # test case minification
    def test_prettify_example25(self):
        self.interpret("../theories/Example4-7.fpl")
        self.assertFalse(self.interpreter.has_errors())
        self.assertFalse(self.interpreter_after_prettify.has_errors())


if __name__ == '__main__':
    unittest.main()
