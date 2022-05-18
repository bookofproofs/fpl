from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class ConjecturesTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_conjectures"

    @parameterized.expand([
        "test_conjecture_01.fpl",
        "test_conjecture_02.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
