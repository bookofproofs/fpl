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
        "test_types_var_decl_02a.fpl",
        "test_types_var_decl_02b.fpl",
        "test_types_var_decl_03.fpl",
        "test_types_var_decl_04.fpl",
        "test_types_var_decl_04a.fpl",
        "test_types_var_decl_04b.fpl",
        "test_types_var_decl_05.fpl",
        "test_types_var_decl_06.fpl",
        "test_types_var_decl_06a.fpl",
        "test_types_var_decl_06b.fpl",
        "test_types_var_decl_07.fpl",
        "test_types_var_decl_07a.fpl",
        "test_types_var_decl_07b.fpl",
        "test_types_var_decl_08.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
