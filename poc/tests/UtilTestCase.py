import unittest
from parameterized import parameterized
from anytree import search
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxSTVarDec import AuxSTVarDec
from poc.util.fplutil import Utils
from poc.fplinterpreter import FplInterpreter
from poc.fplsourcetransformer import FPLSourceTransformer
from tatsu.exceptions import FailedToken
from tatsu.exceptions import FailedParse
from tatsu.exceptions import FailedPattern
import os


class UtilTestCase(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.normpath(os.path.abspath(__file__))
        if os.path.isfile(cls.path):
            cls.path = os.path.dirname(cls.path)
        cls.path_to_grammar = os.path.join(cls.path, "../../grammar")
        cls.path_to_usecases = os.path.join(cls.path)
        cls.util = Utils()
        cls.fpl_parser = cls.util.get_parser(cls.path_to_grammar + "/fpl_tatsu_format.ebnf")
        cls.transformer = FPLSourceTransformer(cls.fpl_parser)

    def syntax_analysis_correct(self, use_case, rewrite=False):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        actual = self.util.adjust_symbol_table_for_testing(interpreter)
        if AuxISourceAnalyser.verbose:
            print(actual)
            if rewrite and result[1].strip() != actual:
                self.util.rewrite_expected_test_case(self.path_to_usecases, use_case, actual)
        else:
            if rewrite:
                self.assertEqual(rewrite,
                                 "Please set rewrite flag to false unless you really want override the expected values")
        self.assertEqual(result[1].strip(), actual)

    def syntax_analysis_correct_node_number(self, use_case, number_of_nodes):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        r = interpreter.get_symbol_table_root()
        globals_node = AuxSymbolTable.get_child_by_outline(r, AuxSTConstants.globals)
        if use_case.endswith("test_robustness_types_var_decl.fpl"):
            r = search.findall(globals_node.children[0].reference, lambda node: isinstance(node, AuxSTVarDec))
            self.assertEqual(number_of_nodes, len(r))
        else:
            self.assertEqual(number_of_nodes, len(globals_node.children))

    def semantical_analysis_detects_fpl_error(self, use_case, diagnose_id):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        interpreter.semantic_analysis()
        if AuxISourceAnalyser.verbose:
            interpreter.get_error_mgr().print_errors()
        # the error is the same as in the use case file
        self.assertTrue(Utils.check_if_error_occurs(result[1], interpreter.get_error_mgr(), diagnose_id))

    def semantical_analysis_detects_no_fpl_error(self, use_case, diagnose_id):
        path_to_use_cases = os.path.join(self.path_to_usecases, use_case)
        interpreter = FplInterpreter(self.fpl_parser, path_to_use_cases)
        result = Utils.get_code_and_expected(self.path_to_usecases, use_case)
        interpreter.syntax_analysis(path_to_use_cases)
        interpreter.semantic_analysis()
        if AuxISourceAnalyser.verbose:
            interpreter.get_error_mgr().print_errors()
        # the error is the same as in the use case file
        self.assertTrue(Utils.check_if_error_does_not_occur(interpreter.get_error_mgr(), diagnose_id))

    def parser_success(self, use_case):
        self.transformer.clear()
        self.transformer.syntax_transform(self.path_to_usecases + "/" + use_case + ".fpl")

    def parser_fail(self, use_case):
        try:
            self.transformer.clear()
            self.transformer.syntax_transform(self.path_to_usecases + "/" + use_case + ".fpl")
        except FailedToken as ex:
            return
        except FailedParse as ex:
            return
        except FailedPattern as ex:
            return
        self.assertFalse(True)
