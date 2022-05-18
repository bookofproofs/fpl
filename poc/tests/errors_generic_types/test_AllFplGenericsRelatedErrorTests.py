from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllFplGenericsRelatedErrorTests(UtilTestCase):
    rewrite = False
    folder = "errors_generic_types"

    @parameterized.expand([
        ("test_FplTemplateMisused_01.fpl", "SE0130"),
        ("test_FplTemplateMisused_02.fpl", "SE0130"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)
