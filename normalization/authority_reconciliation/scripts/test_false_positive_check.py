import unittest

from normalization.authority_reconciliation.scripts.false_positive_check import is_same_entity


class TestFalsePositiveCheckGeognames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity(u"hello", u"hello", controlaccess_type=u"geogname"))

    def test_reordered_match(self):
        self.assertTrue(is_same_entity(u"Ann Arbor (Mich. : Township)", u"Ann Arbor Township (Mich.)", controlaccess_type=u"geogname"))

    def test_township_mismatch(self):
        self.assertFalse(is_same_entity(u"Ann Arbor (Mich.)", u"Ann Arbor Township (Mich.)", controlaccess_type=u"geogname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity(u"Buffalo (N.Y.)", u"Canisus College", controlaccess_type=u"geogname"))


class TestFalsePositiveCheckCorpnames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity(u"United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                       u"United States. Army. Michigan Artillery Regiment, 6th (1863-1865)",
                                       controlaccess_type=u"corpname"))

    def test_match_with_extra_words(self):
        self.assertTrue(is_same_entity(u"New York World's Fair (1939-1940)",
                                       u"New York World's Fair (1939-1940 : New York, N.Y.)",
                                       controlaccess_type=u"corpname"))

    def test_match_with_ampersand(self):
        self.assertTrue(is_same_entity(u"Gunnar Birkerts   Associates.", u"Gunnar Birkerts & Associates", controlaccess_type=u"corpname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity(u"Oberlin College.", u"Allen Memorial Art Museum", controlaccess_type=u"corpname"))

    def test_fuzzy_mismatch(self):
        self.assertFalse(is_same_entity(u"University of Michigan. Gilbert and Sullivan Society.",
                                        u"Friends of the University of Michigan Gilbert and Sullivan Society",
                                        controlaccess_type=u"corpname"))

    def test_wrong_university(self):
        self.assertFalse(is_same_entity(u"University of Michigan. Department of Civil and Environmental Engineering.",
                                        u"Michigan Technological University. Department of Civil and Environmental Engineering",
                                        controlaccess_type=u"corpname"))


class TestFalsePositiveCheckPersnames(unittest.TestCase):
    def test_definite_match(self):
        self.assertTrue(is_same_entity(u"Slichter, Sumner H. (Sumner Huber), 1892-1959.",
                                       u"Slichter, Sumner H. (Sumner Huber), 1892-1959",
                                       controlaccess_type=u"persname"))

    def test_match_with_salutation(self):
        self.assertTrue(is_same_entity(u"Allen, Edward Payson, 1839-1909.",
                                       u"Allen, Mr. (Edward Payson), 1839-1909",
                                       controlaccess_type=u"persname"))

    def test_match_without_paren_name(self):
        self.assertTrue(is_same_entity(u"Altmeyer, Arthur Joseph, 1891-1972.",
                                       u"Altmeyer, Arthur J. (Arthur Joseph), 1891-1972",
                                       controlaccess_type=u"persname"))

    def test_complex_match(self):
        self.assertTrue(is_same_entity(u"Dillman, Grover C., 1889-",
                                       u"Dillman, Grover C. (Grover Cleveland), 1889-1979",
                                       controlaccess_type=u"persname"))

    def test_with_new_deathdate(self):
        self.assertTrue(is_same_entity(u"Bronte, Lydia, 1938-", u"Bronte, Lydia, 1938-2003", controlaccess_type=u"persname"))

    def test_match_without_dates(self):
        self.assertTrue(is_same_entity(u"Danforth, Percy.", u"Danforth, Percy", controlaccess_type=u"persname"))

    def test_definite_mismatch(self):
        self.assertFalse(is_same_entity(u"Wilder, Thornton, 1897-1975.",
                                        u"Williams, Tennessee, 1911-1983",
                                        controlaccess_type=u"persname"))

    def test_partial_mismatch(self):
        self.assertFalse(is_same_entity(u"Brown, Catherine.", u"Tkacz, Catherine Brown", controlaccess_type=u"persname"))

    def test_mismatch_with_dates(self):
        self.assertFalse(is_same_entity(u"Tobin, Daniel J.", u"Tobin, Daniel Joseph, 1875-1955", controlaccess_type=u"persname"))


if __name__ == "__main__":
    unittest.main()
