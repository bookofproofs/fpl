from poc.tests.UtilTestCase import UtilTestCase, parameterized
"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class PropositionsTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_propositions"

    @parameterized.expand([
        "test_proposition_01.fpl",
        "test_proposition_02.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
