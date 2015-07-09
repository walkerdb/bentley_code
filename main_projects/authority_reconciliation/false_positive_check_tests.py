import unittest
from main_projects.authority_reconciliation.false_positive_check import is_same_entity

class TestFalsePositiveCheckGeognames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity("hello", "hello", type="geogname"))

    def test_reordered_match(self):
        self.assertTrue(is_same_entity("Ann Arbor (Mich. : Township)", "Ann Arbor Township (Mich.)", type="geogname"))

    def test_township_mismatch(self):
        self.assertFalse(is_same_entity("Ann Arbor (Mich.)", "Ann Arbor Township (Mich.)", type="geogname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity("Buffalo (N.Y.)", "Canisus College", type="geogname"))


class TestFalsePositiveCheckCorpnames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity("United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                       "United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                       type="corpname"))

    def test_match_with_ampersand(self):
        self.assertTrue(is_same_entity("Gunnar Birkerts   Associates.", "Gunnar Birkerts & Associates", type="corpname"))

    def test_match_with_extra_words(self):
        self.assertTrue(is_same_entity("New York World's Fair (1939-1940)",
                                       "New York World's Fair (1939-1940 : New York, N.Y.)",
                                       type="corpname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity("Oberlin College.", "Allen Memorial Art Museum", type="corpname"))

    def test_fuzzy_mismatch(self):
        self.assertFalse(is_same_entity("University of Michigan. Gilbert and Sullivan Society.",
                                        "Friends of the University of Michigan Gilbert and Sullivan Society",
                                        type="corpname"))

    def test_wrong_university(self):
        self.assertFalse(is_same_entity("University of Michigan. Department of Civil and Environmental Engineering.",
                                        "Michigan Technological University. Department of Civil and Environmental Engineering",
                                        type="corpname"))

if __name__ == "__main__":
    unittest.main()
