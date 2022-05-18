from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class ClassTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_classes"

    @parameterized.expand([
        "test_class_01.fpl",
        "test_class_02.fpl",
        "test_class_03.fpl",
        "test_class_04.fpl",
        "test_class_05.fpl",
        "test_class_06.fpl",
        "test_class_07.fpl",
        "test_class_08.fpl",
        "test_class_09.fpl",
        "test_class_10.fpl",
        "test_class_11.fpl",
        "test_class_12.fpl",
        "test_class_13.fpl",
        "test_class_14.fpl",
        "test_class_15.fpl",
        "test_class_16.fpl",
        "test_class_17.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
