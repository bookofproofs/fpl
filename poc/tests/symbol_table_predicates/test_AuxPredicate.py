import unittest
from parameterized import parameterized
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSymbolTable import AuxSymbolTable
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from anytree import AnyNode

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
        cls.root = AnyNode()
        cls.i = AuxISourceAnalyser([], cls.root, "")
        cls.i.last_positions_by_rule["true"] = cls.aux_info
        cls.i.last_positions_by_rule["false"] = cls.aux_info
        cls.i.last_positions_by_rule["impl"] = cls.aux_info
        cls.i.last_positions_by_rule["Implication"] = cls.aux_info
        cls.i.last_positions_by_rule["not"] = cls.aux_info
        cls.i.last_positions_by_rule["Negation"] = cls.aux_info
        cls.i.last_positions_by_rule["and"] = cls.aux_info
        cls.i.last_positions_by_rule["Conjunction"] = cls.aux_info
        cls.i.last_positions_by_rule["or"] = cls.aux_info
        cls.i.last_positions_by_rule["Disjunction"] = cls.aux_info
        cls.i.last_positions_by_rule["iif"] = cls.aux_info
        cls.i.last_positions_by_rule["Equivalence"] = cls.aux_info
        cls.i.last_positions_by_rule["xor"] = cls.aux_info
        cls.i.last_positions_by_rule["ExclusiveOr"] = cls.aux_info
        cls.i.last_positions_by_rule["ex"] = cls.aux_info
        cls.i.last_positions_by_rule["Exists"] = cls.aux_info
        cls.i.last_positions_by_rule["all"] = cls.aux_info
        cls.i.last_positions_by_rule["All"] = cls.aux_info
        cls.aux_inter = AuxInterpretation(cls.aux_info, cls.i.errors)

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
        p = AuxSTPredicate(p_type, self.i)
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
        p = AuxSTPredicate(p_type, self.i)
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_negation, self.i)
        p = AuxSTPredicate(p_type, self.i)
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_conjunction, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_disjunction, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_equivalence, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_exclusiveOr, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
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
        result = AuxSTPredicate(AuxSymbolTable.predicate_implication, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
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
