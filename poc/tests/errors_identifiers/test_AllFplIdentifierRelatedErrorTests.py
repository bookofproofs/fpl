from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllFplIdentifierRelatedErrorTests(UtilTestCase):
    rewrite = False
    folder = "errors_identifiers"

    @parameterized.expand([
        ("test_FplIdentifierAlreadyDeclared_namespace_usage.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_inference_rule.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_predicate_declaration.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_functional_term.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_axiom.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class_instance_property.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class_instance_template_property.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_class_func_property.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_theorem.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_corollary.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_proposition.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_lemma.fpl", "SE0020"),
        ("test_FplIdentifierAlreadyDeclared_conjecture.fpl", "SE0020"),
        ("test_FplMisspelledConstructor_first_occurrence.fpl", "SE0030"),
        ("test_FplMisspelledConstructor_second_occurrence.fpl", "SE0030"),
        ("test_FplMisspelledProperty_01.fpl", "SE0035"),
        ("test_FplMisspelledProperty_02.fpl", "SE0035"),
        ("test_FplIdentifierNotDeclared_01.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_02.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_03.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_05.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_06.fpl", "SE0090"),
        ("test_FplCorollaryMissingTheoremLikeStatement_01.fpl", "SE0165"),
        ("test_FplMissingProof_01.fpl", "SE0140"),
        ("test_FplMissingProof_02.fpl", "SE0140"),
        ("test_FplMissingProof_03.fpl", "SE0140"),
        ("test_FplMissingProof_04.fpl", "SE0140"),
        ("test_FplProvedConjecture_01.fpl", "SE0150"),
        ("test_FplProofMissingTheoremLikeStatement_01.fpl", "SE0160"),
        ("test_FplAmbiguousSignature_01.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_02.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_03.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_04.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_05.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_06.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_07.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_08.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_09.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_10.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_11.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_12.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_13.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_14.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_15.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_16.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_17.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_18.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_19.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_20.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_21.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_22.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_23.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_24.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_25.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_26.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_27.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_28.fpl", "SE0170"),
        ("test_FplAmbiguousSignature_29.fpl", "SE0170"),
        ("test_FplForbiddenOverride_01.fpl", "SE0180"),
        ("test_FplForbiddenOverride_02.fpl", "SE0180"),
        ("test_FplForbiddenOverride_03.fpl", "SE0180"),
        ("test_FplForbiddenOverride_04.fpl", "SE0180"),
        ("test_FplForbiddenOverride_05.fpl", "SE0180"),
        ("test_FplForbiddenOverride_06.fpl", "SE0180"),
        ("test_FplForbiddenOverride_07.fpl", "SE0180"),
        ("test_FplForbiddenOverride_08.fpl", "SE0180"),
        ("test_FplForbiddenOverride_09.fpl", "SE0180"),
        ("test_FplForbiddenOverride_10.fpl", "SE0180"),
        ("test_FplForbiddenOverride_11.fpl", "SE0180"),
        ("test_FplForbiddenOverride_12.fpl", "SE0180"),
        ("test_FplForbiddenOverride_13.fpl", "SE0180"),
        ("test_FplForbiddenOverride_14.fpl", "SE0180"),
        ("test_FplForbiddenOverride_15.fpl", "SE0180"),
        ("test_FplForbiddenOverride_16.fpl", "SE0180"),
        ("test_FplForbiddenOverride_17.fpl", "SE0180"),
        ("test_FplForbiddenOverride_18.fpl", "SE0180"),
        ("test_FplForbiddenOverride_19.fpl", "SE0180"),
        ("test_FplForbiddenOverride_20.fpl", "SE0180"),
        ("test_FplForbiddenOverride_21.fpl", "SE0180"),
        ("test_FplForbiddenOverride_22.fpl", "SE0180"),
        ("test_FplForbiddenOverride_23.fpl", "SE0180"),
        ("test_FplForbiddenOverride_24.fpl", "SE0180"),
        ("test_FplForbiddenOverride_25.fpl", "SE0180"),
        ("test_FplForbiddenOverride_26.fpl", "SE0180"),
        ("test_FplForbiddenOverride_27.fpl", "SE0180"),
        ("test_FplForbiddenOverride_28.fpl", "SE0180"),
        ("test_FplForbiddenOverride_axiom.fpl", "SE0180"),
        ("test_FplForbiddenOverride_conjecture.fpl", "SE0180"),
        ("test_FplForbiddenOverride_corollary.fpl", "SE0180"),
        ("test_FplForbiddenOverride_lemma.fpl", "SE0180"),
        ("test_FplForbiddenOverride_proposition.fpl", "SE0180"),
        ("test_FplForbiddenOverride_theorem.fpl", "SE0180"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplIdentifierAlreadyDeclared_ok_01.fpl", "SE0020"),
        ("test_FplMisspelledConstructor_ok_01.fpl", "SE0030"),
        ("test_FplMisspelledConstructor_ok_02.fpl", "SE0030"),
        ("test_FplIdentifierNotDeclared_ok_01.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_ok_02.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_ok_03.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_ok_04.fpl", "SE0090"),
        ("test_FplIdentifierNotDeclared_ok_05.fpl", "SE0090"),
        ("test_FplMissingProof_ok_01.fpl", "SE0140"),
        ("test_FplProvedConjecture_ok_01.fpl", "SE0150"),
        ("test_FplProofMissingTheoremLikeStatement_ok_01.fpl", "SE0160"),
        ("test_FplCorollaryMissingTheoremLikeStatement_ok_01.fpl", "SE0165"),
        ("test_FplForbiddenOverride_ok_constructor.fpl", "SE0180"),
        ("test_FplForbiddenOverride_ok_functional_term.fpl", "SE0180"),
        ("test_FplForbiddenOverride_ok_inference_rule.fpl", "SE0180"),
        ("test_FplForbiddenOverride_ok_instance_class.fpl", "SE0180"),
        ("test_FplForbiddenOverride_ok_instance_functional_term.fpl", "SE0180"),
        ("test_FplForbiddenOverride_ok_instance_predicate.fpl", "SE0180"),
        ("test_FplForbiddenOverride_ok_predicate.fpl", "SE0180"),
        ("test_FplForbiddenOverride_ok_property.fpl", "SE0180"),
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
