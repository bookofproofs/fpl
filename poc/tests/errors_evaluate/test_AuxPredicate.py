import unittest
from parameterized import parameterized
from poc.classes.AuxSTPredicate import AuxSTPredicate
from poc.classes.AuxSTConstants import AuxSTConstants
from poc.classes.AuxInterpretation import AuxInterpretation
from poc.classes.AuxAstInfo import AuxAstInfo
from poc.classes.AuxISourceAnalyser import AuxISourceAnalyser
from anytree import AnyNode
from poc.fplsemanticanalyzer import SemanticAnalyser
from poc.fplerror import FplErrorManager
from poc.classes.AuxEvaluation import EvaluateParams
from poc.classes.AuxEvaluationRegister import AuxEvaluationRegister
from poc.classes.AuxInbuiltTypes import InbuiltPredicate
from poc.classes.AuxSTDefinitionPredicate import AuxSTDefinitionPredicate

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

        cls._symbol_table_root = AnyNode(outline=AuxSTConstants.root)
        cls._error_mgr = FplErrorManager()
        node = AnyNode(outline=AuxSTConstants.globals, parent=cls._symbol_table_root)
        cls.analyzer = SemanticAnalyser(cls._symbol_table_root, cls._error_mgr)
        cls.sem = cls.analyzer
        cls.i.last_positions_by_rule["PredicateHeader"] = cls.aux_info
        cls.i.last_positions_by_rule["DefinitionPredicate"] = cls.aux_info
        register = AuxEvaluationRegister(node, None)
        register.building_block = AuxSTDefinitionPredicate(cls.i)
        register.instance_guid = register.building_block.get_main_instance().id
        register.instance = register.building_block.get_instance(register.instance_guid);
        cls.sem.eval_stack.append(register)

    @parameterized.expand([
        AuxSTConstants.predicate_negation,
        AuxSTConstants.predicate_implication,
        AuxSTConstants.predicate_conjunction,
        AuxSTConstants.predicate_disjunction,
        AuxSTConstants.predicate_equivalence,
        AuxSTConstants.predicate_exclusiveOr,
        AuxSTConstants.predicate_exists,
        AuxSTConstants.predicate_all,
        AuxSTConstants.predicate_false,
        AuxSTConstants.predicate_true,
    ])
    def test_assert_revoke(self, p_type: str):
        """
        Tests if asserted predicates always return True and, after they have been revoked, always return False
        :param p_type: any type of predicate used to create one
        :return: None
        """
        p = AuxSTPredicate(p_type, self.i)
        p.assert_predicate()

        ret = EvaluateParams.evaluate_recursion(self.sem, p, expected_type=InbuiltPredicate(p))
        self.assertTrue(ret.value.get_value())
        p.revoke_predicate()

        ret = EvaluateParams.evaluate_recursion(self.sem, p, expected_type=InbuiltPredicate(p))
        self.assertFalse(ret.value.get_value())

    @parameterized.expand([
        AuxSTConstants.predicate_false,
        AuxSTConstants.predicate_true,
    ])
    def test_truth_table_true_false(self, p_type: str):
        """
        Tests the truth table of the negation predicate
        :param p_type: true or false predicate type
        :return: None
        """

        p = AuxSTPredicate(p_type, self.i)
        ret = EvaluateParams.evaluate_recursion(self.sem, p, expected_type=InbuiltPredicate(p))

        if p_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_false:
            self.assertFalse(ret.value.get_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        AuxSTConstants.predicate_false,
        AuxSTConstants.predicate_true,
    ])
    def test_truth_table_negation(self, p_type: str):
        """
        Tests the truth table of the negation predicate
        :param p_type: true or false predicate type
        :return: None
        """
        result = AuxSTPredicate(AuxSTConstants.predicate_negation, self.i)
        p = AuxSTPredicate(p_type, self.i)
        result.register_child(p)

        ret = EvaluateParams.evaluate_recursion(self.sem, result, expected_type=InbuiltPredicate(p))

        if p_type == AuxSTConstants.predicate_true:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_false:
            self.assertTrue(ret.value.get_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_true),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_true),
    ])
    def test_truth_table_conjunction(self, p_type: str, q_type: str):
        """
        Tests the truth table of the conjunction predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxSTPredicate(AuxSTConstants.predicate_conjunction, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
        result.register_child(p)
        result.register_child(q)

        ret = EvaluateParams.evaluate_recursion(self.sem, result, expected_type=InbuiltPredicate(result))

        if p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_false:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_true:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_false:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_true),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_true),
    ])
    def test_truth_table_disjunction(self, p_type: str, q_type: str):
        """
        Tests the truth table of the disjunction predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxSTPredicate(AuxSTConstants.predicate_disjunction, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
        result.register_child(p)
        result.register_child(q)

        ret = EvaluateParams.evaluate_recursion(self.sem, result, expected_type=InbuiltPredicate(result))

        if p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_false:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_false:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_true),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_true),
    ])
    def test_truth_table_equivalence(self, p_type: str, q_type: str):
        """
        Tests the truth table of the equivalence predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxSTPredicate(AuxSTConstants.predicate_equivalence, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
        result.register_child(p)
        result.register_child(q)

        ret = EvaluateParams.evaluate_recursion(self.sem, result, expected_type=InbuiltPredicate(result))

        if p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_false:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_true:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_false:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_true),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_true),
    ])
    def test_truth_table_exclusive_or(self, p_type: str, q_type: str):
        """
        Tests the truth table of the exclusive or predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxSTPredicate(AuxSTConstants.predicate_exclusiveOr, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
        result.register_child(p)
        result.register_child(q)

        ret = EvaluateParams.evaluate_recursion(self.sem, result, expected_type=InbuiltPredicate(result))

        if p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_false:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_false:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_true:
            self.assertFalse(ret.value.get_value())
        else:
            raise NotImplementedError()

    @parameterized.expand([
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_false, AuxSTConstants.predicate_true),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_false),
        (AuxSTConstants.predicate_true, AuxSTConstants.predicate_true),
    ])
    def test_truth_table_implication(self, p_type: str, q_type: str):
        """
        Tests the truth table of the implication predicate
        :param p_type: first predicate type
        :param q_type: second predicate type
        :return: None
        """
        result = AuxSTPredicate(AuxSTConstants.predicate_implication, self.i)
        p = AuxSTPredicate(p_type, self.i)
        q = AuxSTPredicate(q_type, self.i)
        result.register_child(p)
        result.register_child(q)

        ret = EvaluateParams.evaluate_recursion(self.sem, result, expected_type=InbuiltPredicate(result))

        if p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_false:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_false and q_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_false:
            self.assertFalse(ret.value.get_value())
        elif p_type == AuxSTConstants.predicate_true and q_type == AuxSTConstants.predicate_true:
            self.assertTrue(ret.value.get_value())
        else:
            raise NotImplementedError()
