from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllFplExtensionRelatedErrorTests(UtilTestCase):
    rewrite = False
    folder = "errors_extensions"

    @parameterized.expand([
        ("test_FplExtensionExists_01.fpl", "SE0300"),
        ("test_FplExtensionMalformed_01.fpl", "SE0310"),
        ("test_FplExtensionUnknown_01.fpl", "SE0320"),
        ("test_FplExtensionUnknown_02.fpl", "SE0320"),
        ("test_FplExtensionUndeclared_01.fpl", "SE0330"),
        ("test_FplExtensionMissingClass_01.fpl", "SE0340"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplExtensionMissingClass_ok_01.fpl", "SE0340"),
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
