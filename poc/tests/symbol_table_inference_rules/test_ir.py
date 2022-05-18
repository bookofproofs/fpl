from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class InferenceRulesTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_inference_rules"

    @parameterized.expand([
        "test_ir_01.fpl",
        "test_ir_02.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
