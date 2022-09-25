from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllFplVariableRelatedErrors(UtilTestCase):
    rewrite = False
    folder = "errors_variables"

    @parameterized.expand([
        ("test_FplVariableDuplicateInVariableList_constructor_signature.fpl", "SE0010"),
        ("test_FplVariableDuplicateInVariableList_other_signature.fpl", "SE0010"),
        ("test_FplVariableDuplicateInVariableList_var_declaration.fpl", "SE0010"),
        ("test_FplUndeclaredVariable_01.fpl", "SE0070"),
        ("test_FplUndeclaredVariable_02.fpl", "SE0070"),
        ("test_FplUndeclaredVariable_03.fpl", "SE0070"),
        ("test_FplUnusedVariable_01.fpl", "SE0075"),
        ("test_FplUnusedVariable_02.fpl", "SE0075"),
        ("test_FplUnusedVariable_03.fpl", "SE0075"),
        ("test_FplUnusedVariable_04.fpl", "SE0075"),
        ("test_FplUnusedVariable_05.fpl", "SE0075"),
        ("test_FplUnusedVariable_06.fpl", "SE0075"),
        ("test_FplVariableAlreadyDeclared_axiom_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_axiom_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_theorem_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_theorem_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_ir_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_ir_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_03.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_04.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_05.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_06.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_07.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_08.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_03.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_04.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_05.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_06.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_07.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_08.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_lemma_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_lemma_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_proof_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_proof_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_proof_03.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_proof_04.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_proposition_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_proposition_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_conjecture_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_conjecture_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_corollary_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_corollary_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_01.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_02.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_03.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_04.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_05.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_06.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_07.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_08.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_09.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_10.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_class_11.fpl", "SE0080"),
        ("test_FplVariableBound_01.fpl", "SE0270"),
        ("test_FplVariableBound_02.fpl", "SE0270"),
        ("test_FplVariableBound_03.fpl", "SE0270"),
        ("test_FplUnusedBoundVariable_01.fpl", "SE0077"),
        ("test_FplUnusedBoundVariable_02.fpl", "SE0077"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplUndeclaredVariable_ok_01.fpl", "SE0070"),
        ("test_FplUndeclaredVariable_ok_02.fpl", "SE0070"),
        ("test_FplUndeclaredVariable_ok_03.fpl", "SE0070"),
        ("test_FplUnusedVariable_ok_01.fpl", "SE0075"),
        ("test_FplUnusedVariable_ok_02.fpl", "SE0075"),
        ("test_FplUnusedVariable_ok_03.fpl", "SE0075"),
        ("test_FplUnusedVariable_ok_04.fpl", "SE0075"),
        ("test_FplUnusedVariable_ok_05.fpl", "SE0075"),
        ("test_FplUnusedVariable_ok_06.fpl", "SE0075"),
        ("test_FplUnusedVariable_ok_07.fpl", "SE0075"),
        ("test_FplVariableAlreadyDeclared_class_ok.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_predicate_ok.fpl", "SE0080"),
        ("test_FplVariableAlreadyDeclared_functional_term_ok.fpl", "SE0080"),
        ("test_FplVariableBound_ok_01.fpl", "SE0270"),
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
