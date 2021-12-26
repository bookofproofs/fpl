import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os

"""
Tests of FPL related (transformer) errors.
Note: FPL parser is autogenerated through the TatSu package. Therefore, we do not test any FPL syntax errors.
"""


class FplIdentifierAlreadyDeclaredTests(unittest.TestCase):
    path = None
    util = None
    path_to_grammar = None

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.normpath(os.path.abspath(__file__))
        if os.path.isfile(cls.path):
            cls.path = os.path.dirname(cls.path)
        cls.path_to_grammar = os.path.join(cls.path, "../../../grammar")
        cls.path_to_usecases = os.path.join(cls.path)
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser(cls.path_to_grammar + "/fpl_tatsu_format.ebnf")

    @parameterized.expand([
        "test_FplIdentifierAlreadyDeclared_namespace_usage.fpl",
        "test_FplIdentifierAlreadyDeclared_inference_rule.fpl",
        "test_FplIdentifierAlreadyDeclared_class.fpl",
        "test_FplIdentifierAlreadyDeclared_predicate_declaration.fpl",
        "test_FplIdentifierAlreadyDeclared_functional_term.fpl",
        "test_FplIdentifierAlreadyDeclared_axiom.fpl",
        "test_FplIdentifierAlreadyDeclared_class_instance_property.fpl",
        "test_FplIdentifierAlreadyDeclared_class_instance_template_property.fpl",
        "test_FplIdentifierAlreadyDeclared_class_func_property.fpl",
        "test_FplIdentifierAlreadyDeclared_theorem.fpl",
        "test_FplIdentifierAlreadyDeclared_corollary.fpl",
        "test_FplIdentifierAlreadyDeclared_proposition.fpl",
        "test_FplIdentifierAlreadyDeclared_lemma.fpl",
        "test_FplIdentifierAlreadyDeclared_conjecture.fpl",
    ])
    def test_errors(self, use_case):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        # exactly one error was found
        self.assertEqual(1, len(interpreter.get_errors()))
        # the error is the same as in the use case file
        self.assertIn(result[1].strip(), str(interpreter.get_errors()[0]))
