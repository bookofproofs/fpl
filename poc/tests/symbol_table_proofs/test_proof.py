from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class TypeTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_proofs"

    @parameterized.expand([
        "test_proof_01.fpl",
        "test_proof_02.fpl",
        "test_proof_03.fpl",
        "test_proof_04.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
