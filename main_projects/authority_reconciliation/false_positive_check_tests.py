import unittest
from main_projects.authority_reconciliation.false_positive_check import is_same_entity

class TestFalsePositiveCheck(unittest.TestCase):
    def test_definite_match(self):
        self.assertEquals(is_same_entity("hello", "hello"), True)

    def test_reordered_match(self):
        self.assertEquals(is_same_entity("Ann Arbor (Mich. : Township)", "Ann Arbor Township (Mich.)"), True)

    def test_township_mismatch(self):
        self.assertEquals(is_same_entity("Ann Arbor (Mich.)", "Ann Arbor Township (Mich.)"), False)

    def test_definite_mismatch(self):
        self.assertEquals(is_same_entity("Buffalo (N.Y.)", "Canisus College"), False)

if __name__ == "__main__":
    unittest.main()