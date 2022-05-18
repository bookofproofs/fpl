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
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
