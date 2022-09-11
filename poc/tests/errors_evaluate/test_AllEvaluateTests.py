from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllEvaluateTests(UtilTestCase):
    rewrite = False
    folder = "errors_evaluate"

    @parameterized.expand([
        ("test_FplVariableNotInitialized_01.fpl", "SE0230"),
        ("test_FplAxiomNotSatisfiable_01.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_02.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_02a.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_02b.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_02c.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_02d.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_02e.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_03.fpl", "SE0240"),
        ("test_FplPremiseNotSatisfiable_01.fpl", "SE0245"),
        ("test_FplPredicateRecursion_01.fpl", "SE0260"),
        ("test_FplPredicateRecursion_02.fpl", "SE0260"),

    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplVariableNotInitialized_ok_01.fpl", "SE0230"),
        ("test_FplAxiomNotSatisfiable_ok_01.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_ok_02.fpl", "SE0240"),
        ("test_FplPremiseNotSatisfiable_ok_01.fpl", "SE0245"),
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
