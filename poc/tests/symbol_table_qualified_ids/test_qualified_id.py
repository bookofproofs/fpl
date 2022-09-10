from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class QualifiedIdsTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_qualified_ids"

    @parameterized.expand([
        "test_qualified_id_01.fpl",
        "test_qualified_id_02.fpl",
        "test_qualified_id_03.fpl",
        "test_qualified_id_04.fpl",
        "test_qualified_id_05.fpl",
        "test_qualified_id_06.fpl",
        "test_qualified_id_07.fpl",
        "test_qualified_id_08.fpl",
        "test_qualified_id_09a.fpl",
        "test_qualified_id_09b.fpl",
        "test_qualified_id_10a.fpl",
        "test_qualified_id_10b.fpl",
        "test_qualified_id_10c.fpl",
        "test_qualified_id_10d.fpl",
        "test_qualified_id_11.fpl",
        "test_qualified_id_12.fpl",
        "test_qualified_id_13.fpl",
        "test_qualified_id_14a.fpl",
        "test_qualified_id_14b.fpl",
        "test_qualified_id_15a.fpl",
        "test_qualified_id_15b.fpl",
        "test_qualified_id_15c.fpl",
        "test_qualified_id_15d.fpl",
        "test_qualified_id_aliased_01.fpl",
        "test_qualified_id_aliased_02.fpl",
        "test_qualified_id_aliased_03.fpl",
        "test_qualified_id_aliased_04.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
