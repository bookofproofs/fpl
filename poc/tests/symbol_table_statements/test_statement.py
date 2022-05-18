from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class StatementTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_statements"

    @parameterized.expand([
        "test_statement_assert_01.fpl",
        "test_statement_assert_02.fpl",
        "test_statement_assign_01.fpl",
        "test_statement_assign_02.fpl",
        "test_statement_cases_01.fpl",
        "test_statement_cases_02.fpl",
        "test_statement_loop_01.fpl",
        "test_statement_loop_02.fpl",
        "test_statement_loop_03.fpl",
        "test_statement_loop_04.fpl",
        "test_statement_loop_05.fpl",
        "test_statement_python_delegate_01.fpl",
        "test_statement_python_delegate_02.fpl",
        "test_statement_range_01.fpl",
        "test_statement_range_02.fpl",
        "test_statement_range_03.fpl",
        "test_statement_return_01.fpl",
        "test_statement_return_02.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
