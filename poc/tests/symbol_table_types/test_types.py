from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class TypeTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_types"

    @parameterized.expand([
        "test_types_class_01.fpl",
        "test_types_class_02.fpl",
        "test_types_class_03.fpl",
        "test_types_isOperator_01.fpl",
        "test_types_var_decl_01.fpl",
        "test_types_var_decl_02.fpl",
        "test_types_var_decl_03.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
