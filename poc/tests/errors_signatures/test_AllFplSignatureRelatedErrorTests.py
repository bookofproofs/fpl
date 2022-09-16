from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllFplSignatureRelatedErrorTests(UtilTestCase):
    rewrite = False
    folder = "errors_signatures"

    @parameterized.expand([
        ("test_FplWrongArguments_01.fpl", "SE0220"),
        ("test_FplWrongArguments_01a.fpl", "SE0220"),
        ("test_FplWrongArguments_02.fpl", "SE0220"),
        ("test_FplWrongArguments_03.fpl", "SE0220"),
        ("test_FplWrongArguments_03a.fpl", "SE0220"),
        ("test_FplWrongArguments_03b.fpl", "SE0220"),
        ("test_FplWrongArguments_04.fpl", "SE0220"),
        ("test_FplWrongArguments_05.fpl", "SE0220"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplWrongArguments_ok_01.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_01a.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_02.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_03.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_04.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_04a.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_04b.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_04c.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_05.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_05a.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_05b.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_05c.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_05d.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_06.fpl", "SE0220"),
        ("test_FplWrongArguments_ok_07.fpl", "SE0220"),
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
