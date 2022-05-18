from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class FunctionalTermsTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_functional_terms"

    @parameterized.expand([
        "test_func_01.fpl",
        "test_func_02.fpl",
        "test_func_03.fpl",
        "test_func_04.fpl",
        "test_func_05.fpl",
        "test_func_06.fpl",
        "test_func_07.fpl",
        "test_func_08.fpl",
        "test_func_09.fpl",
        "test_func_10.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
