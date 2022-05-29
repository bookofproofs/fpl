from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class PredicatesTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_predicates"

    @parameterized.expand([
        "test_predicate_01.fpl",
        "test_predicate_02.fpl",
        "test_predicate_03.fpl",
        "test_predicate_04.fpl",
        "test_predicate_05.fpl",
        "test_predicate_06.fpl",
        "test_predicate_07.fpl",
        "test_predicate_08.fpl",
        "test_predicate_09.fpl",
        "test_predicate_10.fpl",
        "test_predicate_11.fpl",
        "test_predicate_12.fpl",
        "test_predicate_13.fpl",
        "test_predicate_14.fpl",
        "test_predicate_15.fpl",
        "test_predicate_16.fpl",
        "test_predicate_17.fpl",
        "test_predicate_18.fpl",
        "test_predicate_18a.fpl",
        "test_predicate_18b.fpl",
        "test_predicate_19.fpl",
        "test_predicate_20.fpl",
        "test_predicate_20a.fpl",
        "test_predicate_21.fpl",
        "test_predicate_22.fpl",
        "test_predicate_23.fpl",
        "test_predicate_24.fpl",
        "test_predicate_25.fpl",
        "test_predicate_25a.fpl",
        "test_predicate_25b.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
