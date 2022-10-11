from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllTypesRelatedErrorTests(UtilTestCase):
    rewrite = False
    folder = "errors_types"

    @parameterized.expand([
        ("test_FplTemplateMisused_01.fpl", "SE0130"),
        ("test_FplTemplateMisused_02.fpl", "SE0130"),
        ("test_FplTypeNotAllowed_01.fpl", "SE0200"),
        ("test_FplTypeNotAllowed_02.fpl", "SE0200"),
        ("test_FplTypeNotAllowed_03.fpl", "SE0200"),
        ("test_FplTypeMismatch_01.fpl", "SE0250"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplTypeNotAllowed_ok_01.fpl", "SE0200"),
        ("test_FplTypeNotAllowed_ok_02.fpl", "SE0200"),
        ("test_FplTypeNotAllowed_ok_03.fpl", "SE0200"),
        ("test_FplTypeMismatch_ok_01.fpl", "SE0250"),
        ("test_FplTypeMismatch_ok_02.fpl", "SE0250"),
        ("test_FplTypeMismatch_ok_03.fpl", "SE0250"),
        ("test_FplTypeMismatch_ok_04.fpl", "SE0250"),
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
