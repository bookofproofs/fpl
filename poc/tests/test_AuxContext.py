import unittest
from poc.classes.AuxContext import AuxContext

"""
Tests if the parsing context works properly.
"""


class AuxContextTests(unittest.TestCase):

    # test parsing context
    def test_is_parsing_context(self):
        """
        Test if parsing context returns correct results
        """
        sem = AuxContext()
        sem.push_context("t1")
        sem.push_context("t2")
        sem.push_context("t3")
        sem.push_context("t4")
        self.assertTrue(sem.is_parsing_context(["t4"]))
        self.assertTrue(sem.is_parsing_context(["t3", "t4"]))
        self.assertTrue(sem.is_parsing_context(["t2", "t3", "t4"]))
        self.assertTrue(sem.is_parsing_context(["t1", "t2", "t3", "t4"]))
        self.assertFalse(sem.is_parsing_context(["t1"]))
        self.assertFalse(sem.is_parsing_context(["t2"]))
        self.assertFalse(sem.is_parsing_context(["t3"]))
        self.assertFalse(sem.is_parsing_context(["t2", "t3"]))
        self.assertFalse(sem.is_parsing_context(["t0", "t1", "t2", "t3", "t4"]))
        self.assertFalse(sem.is_parsing_context(["t0", "t2", "t3", "t4"]))
        self.assertFalse(sem.is_parsing_context(["t1", "t2", "t3", "t5"]))
        self.assertFalse(sem.is_parsing_context(["t1", "t2", "t", "t4"]))
        self.assertFalse(sem.is_parsing_context(["t1", "t", "t3", "t4"]))

    def test_pop_context(self):
        """
        Test if parsing context returns correct results
        """
        sem = AuxContext()
        sem.push_context("t1")
        sem.push_context("t2")
        sem.push_context("t3")
        sem.push_context("t4")
        with self.assertRaises(AssertionError) as t:
            sem.pop_context(["t1"])
        with self.assertRaises(AssertionError) as t:
            sem.pop_context(["t2"])
        with self.assertRaises(AssertionError) as t:
            sem.pop_context(["t3"])
        sem.pop_context(["t4"])
        sem.pop_context(["t1", "t2", "t3"])
        self.assertEqual(0, len(sem.get_context()))


if __name__ == '__main__':
    unittest.main()
