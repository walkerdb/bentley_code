# coding=utf-8
import unittest
from normalization.authority_reconciliation.scripts.auth_search import AuthoritySearcher


class TestAuthoritySearcher(unittest.TestCase):
    def setUp(self):
        self.auth_search = AuthoritySearcher()
        self.subjects = {(u"geogname", "geogname"),
                         (u"persname", "persname"),
                         (u"corpname", "corpname"),
                         (u"Dickinson, Emily, 1830-1886", "persname"),
                         (u"Google, Inc.", "corpname"),
                         (u"Ann Arbor, Mich.", "geogname")}

    def test_no_results_raises_empty_string(self):
        self.assertEquals(self.auth_search.search_viaf_for_lc_id(u"fake_name", u"geographicNames"), "")

    def test_valid_search_returns_lc_id(self):
        result = self.auth_search.search_viaf_for_lc_id(u"Dickinson, Emily, 1830-1886", u"personalNames")
        self.assertEquals(result, u"n79054166")

    def test_search_with_special_characters(self):
        viaf_result = self.auth_search.search_viaf_for_lc_id(u"Chopin, Frédéric François (1810-1849)", u"personalNames")
        self.assertEquals(viaf_result, u"n79127769")

        lc_result = self.auth_search.retrieve_lc_name(u"n79127769")


    def test_large_search_returns_all_results(self):
        intended_results = {(u'corpname', u'Google, Inc.', u'Google (Firm)'),
                            (u'geogname', u'Ann Arbor, Mich.', u'Ann Arbor (Mich.)'),
                            (u'persname', u'Dickinson, Emily, 1830-1886', u'Dickinson, Emily, 1830-1886')}

        self.assertEquals(self.auth_search.get_lc_authorized_names(self.subjects), intended_results)
