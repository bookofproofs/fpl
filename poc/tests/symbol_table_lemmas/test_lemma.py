from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class LemmasTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_lemmas"

    @parameterized.expand([
        "test_lemma_01.fpl",
        "test_lemma_02.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
