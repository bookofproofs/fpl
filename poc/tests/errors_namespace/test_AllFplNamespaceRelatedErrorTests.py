from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class AllFplNamespaceRelatedErrorTests(UtilTestCase):
    rewrite = False
    folder = "errors_namespace"

    @parameterized.expand([
        ("test_FplMalformedGlobalId_class_namespace.fpl", "SE0040"),
        ("test_FplMalformedGlobalId_property_namespace.fpl", "SE0040"),
        ("test_FplNamespaceNotFound_01.fpl", "SE0110"),
        ("test_FplMalformedNamespace_01.fpl", "SE0120"),
        ("test_FplMalformedNamespace_02.fpl", "SE0120"),
        ("test_FplMalformedNamespace_03.fpl", "SE0120"),
    ])
    def test_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_fpl_error(self.folder + "/" + use_case, diagnose_id)

    @parameterized.expand([
        ("test_FplMalformedGlobalId_constructor_is_ok.fpl", "SE0040")
    ])
    def test_no_errors(self, use_case, diagnose_id):
        super().semantical_analysis_detects_no_fpl_error(self.folder + "/" + use_case, diagnose_id)
