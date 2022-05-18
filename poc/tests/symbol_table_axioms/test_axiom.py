from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AxiomTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_axioms"

    @parameterized.expand([
        "test_axiom_01.fpl",
        "test_axiom_02.fpl",
        "test_axiom_03.fpl",
        "test_axiom_04.fpl",
        "test_axiom_05.fpl",
        "test_axiom_06.fpl",
        "test_axiom_07.fpl",
        "test_axiom_08.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
