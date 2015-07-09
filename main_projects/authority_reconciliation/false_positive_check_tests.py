import unittest
from main_projects.authority_reconciliation.false_positive_check import is_same_entity

class TestFalsePositiveCheckGeognames(unittest.TestCase):
    def test_definite_match(self):
        self.assertEquals(is_same_entity("hello", "hello", type="geogname"), True)

    def test_reordered_match(self):
        self.assertEquals(is_same_entity("Ann Arbor (Mich. : Township)", "Ann Arbor Township (Mich.)", type="geogname"), True)

    def test_township_mismatch(self):
        self.assertEquals(is_same_entity("Ann Arbor (Mich.)", "Ann Arbor Township (Mich.)", type="geogname"), False)

    def test_definite_mismatch(self):
        self.assertEquals(is_same_entity("Buffalo (N.Y.)", "Canisus College", type="geogname"), False)


class TestFalsePositiveCheckCorpnames(unittest.TestCase):
    def test_definite_match(self):
        self.assertEquals(is_same_entity("United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                         "United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                         type="corpname"), True)

    # def test_match_with_different_wording(self):
    #     self.assertEquals(is_same_entity("National Archives (U.S.)", "United States. National Archives and Records Service", type="corpname"), True)

    def test_match_with_ampersand(self):
        self.assertEquals(is_same_entity("Gunnar Birkerts   Associates.", "Gunnar Birkerts & Associates", type="corpname"), True)

    def test_match_with_extra_words(self):
        self.assertEquals(is_same_entity("New York World's Fair (1939-1940)",
                                         "New York World's Fair (1939-1940 : New York, N.Y.)",
                                         type="corpname"), True)

    def test_definite_mismatch(self):
        self.assertEquals(is_same_entity("Oberlin College.", "Allen Memorial Art Museum", type="corpname"), False)

    def test_fuzzy_mismatch(self):
        self.assertEquals(is_same_entity("University of Michigan. Gilbert and Sullivan Society.",
                                         "Friends of the University of Michigan Gilbert and Sullivan Society",
                                         type="corpname"), False)

    def test_wrong_university(self):
        self.assertEquals(is_same_entity("University of Michigan. Department of Civil and Environmental Engineering.",
                                         "Michigan Technological University. Department of Civil and Environmental Engineering",
                                         type="corpname"), False)

if __name__ == "__main__":
    unittest.main()