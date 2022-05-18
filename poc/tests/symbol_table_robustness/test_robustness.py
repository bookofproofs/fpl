from poc.tests.UtilTestCase import UtilTestCase, parameterized, unittest
"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class RobustnessTests(UtilTestCase):
    folder = "symbol_table_robustness"

    @parameterized.expand([
        ("test_robustness_axiom.fpl", 300),
        ("test_robustness_class.fpl", 600),
        ("test_robustness_constructor.fpl", 600),
        ("test_robustness_functional_term.fpl", 300),
        ("test_robustness_inference_rules.fpl", 129),
        ("test_robustness_isOperator.fpl", 299),
        ("test_robustness_predicate.fpl", 556),
        ("test_robustness_proof.fpl", 300),
        ("test_robustness_property_class_instance.fpl", 900),
        ("test_robustness_property_functional_term.fpl", 900),
        ("test_robustness_property_predicate.fpl", 900),
        ("test_robustness_statement_assertion.fpl", 300),
        ("test_robustness_statement_assignment.fpl", 300),
        ("test_robustness_statement_cases.fpl", 100),
        ("test_robustness_statement_loop.fpl", 100),
        ("test_robustness_statement_python_delegate.fpl", 300),
        ("test_robustness_statement_range.fpl", 100),
        ("test_robustness_statement_return.fpl", 300),
        ("test_robustness_theoremlike.fpl", 300),
        ("test_robustness_types_class.fpl", 192),
        ("test_robustness_types_image.fpl", 309),
        ("test_robustness_types_properties.fpl", 315),
        ("test_robustness_types_var_decl.fpl", 1104),
        ("test_robustness_types_var_in_signature.fpl", 309),
        ("test_robustness_uses_clause.fpl", 0),
    ])
    @unittest.skip("Skipping tests for performance reasons, comment this line out to include this test.")
    def test_correct(self, use_case, number_of_nodes):
        super().syntax_analysis_correct_node_number(self.folder + "/" + use_case, number_of_nodes)

