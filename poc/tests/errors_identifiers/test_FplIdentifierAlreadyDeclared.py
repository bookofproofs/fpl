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
        ("test_FplIdentifierAlreadyDeclared_namespace_usage.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_inference_rule.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_predicate_declaration.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_functional_term.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_axiom.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class_instance_property.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class_instance_template_property.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class_func_property.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_theorem.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_corollary.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_proposition.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_lemma.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_conjecture.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_in_other_namespace.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_other.fpl", "SE0020"),
    ])
    def test_errors(self, use_case, diagnose_id):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        interpreter.semantic_analysis()
        # the error is the same as in the use case file
        self.assertTrue(Utils.check_if_error_occurs(result[1], interpreter.get_error_mgr(), diagnose_id))
