import unittest
from parameterized import parameterized
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
import os
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser

"""
Tests of FPL related (transformer) errors.
Note: FPL parser is autogenerated through the TatSu package. Therefore, we do not test any FPL syntax errors.
"""


class FplInvalidInheritanceTests(unittest.TestCase):
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
        ("test_FplInvalidInheritance_func.fpl", "SE0050"),
        ("test_FplInvalidInheritance_function.fpl", "SE0050"),
        ("test_FplInvalidInheritance_pred.fpl", "SE0050"),
        ("test_FplInvalidInheritance_predicate.fpl", "SE0050"),
        ("test_FplInvalidInheritance_tpl.fpl", "SE0050"),
        ("test_FplInvalidInheritance_template.fpl", "SE0050"),
        ("test_FplInvalidInheritance_tpl_capsid.fpl", "SE0050"),
        ("test_FplInvalidInheritance_template_capsid.fpl", "SE0050"),
        ("test_FplInvalidInheritance_tpl_digit.fpl", "SE0050"),
        ("test_FplInvalidInheritance_template_digit.fpl", "SE0050"),
        ("test_FplInvalidInheritance_xid.fpl", "SE0050"),
    ])
    def test_errors(self, use_case, diagnose_id):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        interpreter.semantic_analysis()
        if AuxISourceAnalyser.verbose:
            interpreter.get_error_mgr().print_errors()
        # the error is the same as in the use case file
        self.assertTrue(Utils.check_if_error_occurs(result[1], interpreter.get_error_mgr(), diagnose_id))
