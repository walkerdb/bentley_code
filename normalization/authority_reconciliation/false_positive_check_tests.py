import unittest

from normalization.authority_reconciliation.false_positive_check import is_same_entity


class TestFalsePositiveCheckGeognames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity("hello", "hello", controlaccess_type="geogname"))

    def test_reordered_match(self):
        self.assertTrue(is_same_entity("Ann Arbor (Mich. : Township)", "Ann Arbor Township (Mich.)", controlaccess_type="geogname"))

    def test_township_mismatch(self):
        self.assertFalse(is_same_entity("Ann Arbor (Mich.)", "Ann Arbor Township (Mich.)", controlaccess_type="geogname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity("Buffalo (N.Y.)", "Canisus College", controlaccess_type="geogname"))


class TestFalsePositiveCheckCorpnames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity("United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                       "United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                       controlaccess_type="corpname"))

    def test_match_with_extra_words(self):
        self.assertTrue(is_same_entity("New York World's Fair (1939-1940)",
                                       "New York World's Fair (1939-1940 : New York, N.Y.)",
                                       controlaccess_type="corpname"))

    def test_match_with_ampersand(self):
        self.assertTrue(is_same_entity("Gunnar Birkerts   Associates.", "Gunnar Birkerts & Associates", controlaccess_type="corpname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity("Oberlin College.", "Allen Memorial Art Museum", controlaccess_type="corpname"))

    def test_fuzzy_mismatch(self):
        self.assertFalse(is_same_entity("University of Michigan. Gilbert and Sullivan Society.",
                                        "Friends of the University of Michigan Gilbert and Sullivan Society",
                                        controlaccess_type="corpname"))

    def test_wrong_university(self):
        self.assertFalse(is_same_entity("University of Michigan. Department of Civil and Environmental Engineering.",
                                        "Michigan Technological University. Department of Civil and Environmental Engineering",
                                        controlaccess_type="corpname"))


class TestFalsePositiveCheckPersnames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity("Slichter, Sumner H. (Sumner Huber), 1892-1959.",
                                       "Slichter, Sumner H. (Sumner Huber), 1892-1959",
                                       controlaccess_type="persname"))

    def test_match_with_salutation(self):
        self.assertTrue(is_same_entity("Allen, Edward Payson, 1839-1909.",
                                       "Allen, Mr. (Edward Payson), 1839-1909",
                                       controlaccess_type="persname"))

    def test_match_without_paren_name(self):
        self.assertTrue(is_same_entity("Altmeyer, Arthur Joseph, 1891-1972.",
                                       "Altmeyer, Arthur J. (Arthur Joseph), 1891-1972",
                                       controlaccess_type="persname"))

    def test_complex_match(self):
        self.assertTrue(is_same_entity("Dillman, Grover C., 1889-",
                                       "Dillman, Grover C. (Grover Cleveland), 1889-1979",
                                       controlaccess_type="persname"))

    def test_with_new_deathdate(self):
        self.assertTrue(is_same_entity("Bronte, Lydia, 1938-", "Bronte, Lydia, 1938-2003", controlaccess_type="persname"))

    def test_match_without_dates(self):
        self.assertTrue(is_same_entity("Danforth, Percy.", "Danforth, Percy", controlaccess_type="persname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity("Wilder, Thornton, 1897-1975.",
                                        "Williams, Tennessee, 1911-1983",
                                        controlaccess_type="persname"))

    def test_partial_mismatch(self):
        self.assertFalse(is_same_entity("Brown, Catherine.", "Tkacz, Catherine Brown", controlaccess_type="persname"))

    def test_mismatch_with_dates(self):
        self.assertFalse(is_same_entity("Tobin, Daniel J.", "Tobin, Daniel Joseph, 1875-1955", controlaccess_type="persname"))


if __name__ == "__main__":
    unittest.main()
