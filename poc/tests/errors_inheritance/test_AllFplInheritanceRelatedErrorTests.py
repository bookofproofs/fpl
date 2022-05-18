from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllFplInheritanceRelatedErrorTests(UtilTestCase):
    rewrite = False
    folder = "errors_inheritance"

    @parameterized.expand([
        ("test_FplInvalidInheritance_func.fpl", "SE0050"),
        ("test_FplInvalidInheritance_function.fpl", "SE0050"),
        ("test_FplInvalidInheritance_pred.fpl", "SE0050"),
        ("test_FplInvalidInheritance_predicate.fpl", "SE0050"),
        ("test_FplInvalidInheritance_tpl.fpl", "SE0050"),
        ("test_FplInvalidInheritance_template.fpl", "SE0050"),
        ("test_FplInvalidInheritance_tpl_capsid.fpl", "SE0050"),
        ("test_FplInvalidInheritance_template_capsid.fpl", "SE0050"),
        ("test_FplInvalidInheritance_tpl_digit.fpl", "SE0050"),
        ("test_FplInvalidInheritance_template_digit.fpl", "SE0050"),
        ("test_FplInvalidInheritance_xid.fpl", "SE0050"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)


