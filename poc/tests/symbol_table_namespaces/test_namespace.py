from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class NamespaceTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_namespaces"

    @parameterized.expand([
        "test_namespace_01.fpl",
        "test_namespace_02.fpl",
        "test_namespace_03.fpl",
        "test_namespace_04.fpl",
        "test_namespace_05.fpl",
        "test_namespace_06.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
