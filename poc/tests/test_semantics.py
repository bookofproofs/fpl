import unittest
from fplsemantics import FPLSemantics

"""
Tests if the parsing context works properly.
"""


class SemanticsTests(unittest.TestCase):

    # test parsing context
    def test_is_parsing_context(self):
        """
        Test if parsing context returns correct results
        """
        sem = FPLSemantics()
        sem.push_context("t1", 1)
        sem.push_context("t2", 2)
        sem.push_context("t3", 3)
        sem.push_context("t4", 4)
        self.assertTrue(sem.is_parsing_context("t4"))
        self.assertTrue(sem.is_parsing_context("t3", "t4"))
        self.assertTrue(sem.is_parsing_context("t2", "t3", "t4"))
        self.assertTrue(sem.is_parsing_context("t1", "t2", "t3", "t4"))
        self.assertFalse(sem.is_parsing_context("t0", "t1", "t2", "t3", "t4"))
        self.assertFalse(sem.is_parsing_context("t0", "t2", "t3", "t4"))
        self.assertFalse(sem.is_parsing_context("t1", "t2", "t3", "t5"))
        self.assertFalse(sem.is_parsing_context("t1", "t2", "t", "t4"))
        self.assertFalse(sem.is_parsing_context("t1", "t", "t3", "t4"))
        d = sem.pop_context()
        self.assertEqual(d['key'], "t4")
        self.assertEqual(d['val'], 4)
        d = sem.pop_context()
        self.assertEqual(d['key'], "t3")
        self.assertEqual(d['val'], 3)
        d = sem.pop_context()
        self.assertEqual(d['key'], "t2")
        self.assertEqual(d['val'], 2)
        d = sem.pop_context()
        self.assertEqual(d['key'], "t1")
        self.assertEqual(d['val'], 1)
        d = sem.pop_context()
        self.assertIsNone(d)


if __name__ == '__main__':
    unittest.main()
