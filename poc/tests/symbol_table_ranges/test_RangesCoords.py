from poc.tests.UtilTestCase import UtilTestCase, parameterized

"""
Tests creating the symbol table for randomly derived FPL syntax
"""


class RangesTests(UtilTestCase):
    rewrite = False
    folder = "symbol_table_ranges"

    @parameterized.expand([
        "test_RangesCoords_01.fpl",
        "test_RangesCoords_01a.fpl",
        "test_RangesCoords_02.fpl",
        "test_RangesCoords_02a.fpl",
        "test_RangesCoords_03.fpl",
        "test_RangesCoords_03a.fpl",
        "test_RangesCoords_03b.fpl",
        "test_RangesCoords_03ba.fpl",
        "test_RangesCoords_03c.fpl",
        "test_RangesCoords_03ca.fpl",
        "test_RangesCoords_03d.fpl",
        "test_RangesCoords_03da.fpl",
        "test_RangesCoords_10.fpl",
        "test_RangesCoords_10a.fpl",
        "test_RangesCoords_11.fpl",
        "test_RangesCoords_11a.fpl",
        "test_RangesCoords_12.fpl",
        "test_RangesCoords_12a.fpl",
        "test_RangesCoords_12b.fpl",
        "test_RangesCoords_12ba.fpl",
        "test_RangesCoords_12c.fpl",
        "test_RangesCoords_12ca.fpl",
        "test_RangesCoords_12d.fpl",
        "test_RangesCoords_12da.fpl",
    ])
    def test_correct(self, use_case):
        super().syntax_analysis_correct(self.folder + "/" + use_case, self.rewrite)
