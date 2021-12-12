import unittest
from parameterized import parameterized
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxAstInfo import AuxAstInfo

"""
Tests of FPL implementation of the predicate auxiliary class
"""


class DummyTokenizer:
    def __init__(self):
        self.col = 0
        self.line = 0


class DummyContext:
    def __init__(self):
        self.rule = []
        self.rule.append("")
        self.pos = 0
        self.cst = ""
        self.tokenizer = DummyTokenizer()


class AuxPredicateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.aux_info = AuxAstInfo(DummyContext(), "")
        cls.aux_inter = AuxInterpretation(cls.aux_info, [])

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
        p = AuxSTPredicate(p_type, self.aux_inter)
        p.assert_predicate()
        self.assertTrue(p.evaluate())
        p.revoke_predicate()
        self.assertFalse(p.evaluate())

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
        p = AuxSTPredicate(p_type, self.aux_inter)
        if p_type == AuxSymbolTable.predicate_true:
            self.assertTrue(p.evaluate())
        elif p_type == AuxSymbolTable.predicate_false:
            self.assertFalse(p.evaluate())
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_negation, self.aux_inter)
        p = AuxSTPredicate(p_type, self.aux_inter)
        result.register_child(p)
        if p_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.evaluate())
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_conjunction, self.aux_inter)
        p = AuxSTPredicate(p_type, self.aux_inter)
        q = AuxSTPredicate(q_type, self.aux_inter)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.evaluate())
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_disjunction, self.aux_inter)
        p = AuxSTPredicate(p_type, self.aux_inter)
        q = AuxSTPredicate(q_type, self.aux_inter)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.evaluate())
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_equivalence, self.aux_inter)
        p = AuxSTPredicate(p_type, self.aux_inter)
        q = AuxSTPredicate(q_type, self.aux_inter)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.evaluate())
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_exclusiveOr, self.aux_inter)
        p = AuxSTPredicate(p_type, self.aux_inter)
        q = AuxSTPredicate(q_type, self.aux_inter)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertFalse(result.evaluate())
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_implication, self.aux_inter)
        p = AuxSTPredicate(p_type, self.aux_inter)
        q = AuxSTPredicate(q_type, self.aux_inter)
        result.register_child(p)
        result.register_child(q)
        if p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_false:
            self.assertTrue(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_false and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_false:
            self.assertFalse(result.evaluate())
        elif p_type == AuxSymbolTable.predicate_true and q_type == AuxSymbolTable.predicate_true:
            self.assertTrue(result.evaluate())
        else:
            raise NotImplementedError()
