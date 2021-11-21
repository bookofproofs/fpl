import unittest
from parameterized import parameterized
from poc.classes.AuxPredicate import AuxPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable

"""
Tests of FPL implementation of the predicate auxiliary class
"""


class AuxPredicateTests(unittest.TestCase):

    @parameterized.expand([
        AuxSymbolTable.predicate_negation,
        AuxSymbolTable.predicate_implication,
        AuxSymbolTable.predicate_conjunction,
        AuxSymbolTable.predicate_disjunction,
        AuxSymbolTable.predicate_equivalence,
        AuxSymbolTable.predicate_exclusiveOr,
        AuxSymbolTable.predicate_exists,
        AuxSymbolTable.predicate_all,
        AuxSymbolTable.predicate_false,
        AuxSymbolTable.predicate_true,
    ])
    def test_assert_revoke(self, p_type: str):
        """
        Tests if asserted predicates always return True and, after they have been revoked, always return False
        :param p_type: any type of predicate used to create one
        :return: None
        """
        p = AuxPredicate(p_type)
        p.assert_predicate()
        self.assertTrue(p.get_predicate_value())
        p.revoke_predicate()
        self.assertFalse(p.get_predicate_value())

    @parameterized.expand([
        AuxSymbolTable.predicate_false,
        AuxSymbolTable.predicate_true,
    ])
    def test_truth_table_true_false(self, p_type: str):
        """
        Tests the truth table of the negation predicate
        :param p_type: true or false predicate type
        :return: None
        """
        p = AuxPredicate(p_type)
        if p_type == AuxSymbolTable.predicate_true:
            self.assertTrue(p.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_false:
            self.assertFalse(p.get_predicate_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        AuxSymbolTable.predicate_false,
        AuxSymbolTable.predicate_true,
    ])
    def test_truth_table_negation(self, p_type: str):
        """
        Tests the truth table of the negation predicate
        :param p_type: true or false predicate type
        :return: None
        """
        result = AuxPredicate(AuxSymbolTable.predicate_negation)
        p = AuxPredicate(p_type)
        result.register_child(p)
        if p_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.get_predicate_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_true),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_true),
    ])
    def test_truth_table_conjunction(self, p_type: str, q_type: str):
        """
        Tests the truth table of the conjunction predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxPredicate(AuxSymbolTable.predicate_conjunction)
        p = AuxPredicate(p_type)
        q = AuxPredicate(q_type)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.get_predicate_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_true),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_true),
    ])
    def test_truth_table_disjunction(self, p_type: str, q_type: str):
        """
        Tests the truth table of the disjunction predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxPredicate(AuxSymbolTable.predicate_disjunction)
        p = AuxPredicate(p_type)
        q = AuxPredicate(q_type)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.get_predicate_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_true),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_true),
    ])
    def test_truth_table_equivalence(self, p_type: str, q_type: str):
        """
        Tests the truth table of the equivalence predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxPredicate(AuxSymbolTable.predicate_equivalence)
        p = AuxPredicate(p_type)
        q = AuxPredicate(q_type)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.get_predicate_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_true),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_true),
    ])
    def test_truth_table_exclusive_or(self, p_type: str, q_type: str):
        """
        Tests the truth table of the exclusive or predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxPredicate(AuxSymbolTable.predicate_exclusiveOr)
        p = AuxPredicate(p_type)
        q = AuxPredicate(q_type)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.get_predicate_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_false, AuxSymbolTable.predicate_true),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_false),
        (AuxSymbolTable.predicate_true, AuxSymbolTable.predicate_true),
    ])
    def test_truth_table_implication(self, p_type: str, q_type: str):
        """
        Tests the truth table of the implication predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxPredicate(AuxSymbolTable.predicate_implication)
        p = AuxPredicate(p_type)
        q = AuxPredicate(q_type)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.get_predicate_value())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.get_predicate_value())
        else:
            raise NotImplementedError()
