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
        ("test_FplAxiomNotSatisfiable_04.fpl", "SE0240"),
        ("test_FplPremiseNotSatisfiable_01.fpl", "SE0245"),
        ("test_FplIllegalRecursion_01.fpl", "SE0260"),
        ("test_FplIllegalRecursion_02.fpl", "SE0260"),

    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplVariableNotInitialized_ok_01.fpl", "SE0230"),
        ("test_FplAxiomNotSatisfiable_ok_01.fpl", "SE0240"),
        ("test_FplAxiomNotSatisfiable_ok_02.fpl", "SE0240"),
        ("test_FplPremiseNotSatisfiable_ok_01.fpl", "SE0245"),
        ("test_robustness_assignment_ok_01.fpl", "unknown"),
        ("test_robustness_axiom_ok_01.fpl", "unknown"),
        ("test_robustness_class_ok_01.fpl", "unknown"),
        ("test_robustness_index_var_ok_01.fpl", "unknown"),
        ("test_robustness_proof_ok_01.fpl", "unknown"),
        ("test_robustness_python_delegate_ok_01.fpl", "unknown"),
        ("test_robustness_python_delegate_ok_02.fpl", "unknown"),
        ("test_robustness_range_ok_01.fpl", "unknown"),
        ("test_robustness_range_ok_02.fpl", "unknown"),
        ("test_robustness_range_ok_03.fpl", "unknown"),
        ("test_robustness_self_ok_01.fpl", "unknown"),
        ("test_robustness_self_ok_02.fpl", "unknown"),
        ("test_robustness_type_ok_01.fpl", "unknown"),
        ("test_robustness_type_ok_02.fpl", "unknown"),
        ("test_robustness_type_ok_03.fpl", "unknown"),
        ("test_robustness_type_ok_04.fpl", "unknown"),
        ("test_robustness_type_ok_05.fpl", "unknown"),
        ("test_robustness_type_ok_05a.fpl", "unknown"),
        ("test_robustness_type_ok_05b.fpl", "unknown"),
        ("test_robustness_type_ok_05x.fpl", "unknown"),
        ("test_robustness_type_ok_05ax.fpl", "unknown"),
        ("test_robustness_type_ok_05bx.fpl", "unknown"),
        ("test_robustness_type_ok_05y.fpl", "unknown"),
        ("test_robustness_type_ok_05ay.fpl", "unknown"),
        ("test_robustness_type_ok_05by.fpl", "unknown"),
        ("test_robustness_type_ok_06.fpl", "unknown"),
        ("test_robustness_type_ok_07.fpl", "unknown"),
        ("test_robustness_type_ok_07a.fpl", "unknown"),
        ("test_robustness_type_ok_07b.fpl", "unknown"),
        ("test_robustness_type_ok_07x.fpl", "unknown"),
        ("test_robustness_type_ok_07ax.fpl", "unknown"),
        ("test_robustness_type_ok_07bx.fpl", "unknown"),
        ("test_robustness_type_ok_07y.fpl", "unknown"),
        ("test_robustness_type_ok_07ay.fpl", "unknown"),
        ("test_robustness_type_ok_07by.fpl", "unknown"),
        ("test_robustness_type_ok_08.fpl", "unknown"),
        ("test_robustness_type_ok_08x.fpl", "unknown"),
        ("test_robustness_type_ok_08y.fpl", "unknown"),
        ("test_robustness_type_ok_09.fpl", "unknown"),
        ("test_robustness_type_ok_09x.fpl", "unknown"),
        ("test_robustness_type_ok_09y.fpl", "unknown"),
        ("test_robustness_type_ok_09a.fpl", "unknown"),
        ("test_robustness_type_ok_09ax.fpl", "unknown"),
        ("test_robustness_type_ok_09ay.fpl", "unknown"),
        ("test_robustness_type_ok_09b.fpl", "unknown"),
        ("test_robustness_type_ok_09bx.fpl", "unknown"),
        ("test_robustness_type_ok_09by.fpl", "unknown"),
        ("test_robustness_type_ok_10.fpl", "unknown"),
        ("test_robustness_type_ok_10x.fpl", "unknown"),
        ("test_robustness_type_ok_10y.fpl", "unknown"),
        ("test_robustness_type_ok_10a.fpl", "unknown"),
        ("test_robustness_type_ok_10ax.fpl", "unknown"),
        ("test_robustness_type_ok_10ay.fpl", "unknown"),
        ("test_robustness_type_ok_10b.fpl", "unknown"),
        ("test_robustness_type_ok_10bx.fpl", "unknown"),
        ("test_robustness_type_ok_10by.fpl", "unknown"),
        ("test_robustness_loop_ok_01.fpl", "unknown"),
        ("test_robustness_loop_ok_01a.fpl", "unknown"),
        ("test_robustness_loop_ok_02.fpl", "unknown"),
        ("test_robustness_loop_ok_03.fpl", "unknown"),
        ("test_robustness_loop_ok_04.fpl", "unknown"),
        ("test_robustness_loop_ok_05.fpl", "unknown"),
        ("test_robustness_loop_ok_06.fpl", "unknown"),
        ("test_robustness_loop_ok_07.fpl", "unknown"),
        ("test_robustness_loop_ok_08.fpl", "unknown"),
        ("test_robustness_assertion_ok_01.fpl", "unknown"),
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
