# coding=utf-8
import unittest
from normalization.authority_reconciliation.scripts.auth_search import AuthoritySearcher


class TestAuthoritySearcher(unittest.TestCase):
    def setUp(self):
        self.auth_search = AuthoritySearcher()

    def test_no_results_raises_empty_string(self):
        self.assertEquals(self.auth_search.search_viaf_for_lc_id(u"fake_name", u"geographicNames"), "")

    def test_valid_search_returns_lc_id(self):
        result = self.auth_search.search_viaf_for_lc_id(u"Dickinson, Emily, 1830-1886", u"personalNames")
        self.assertEquals(result, u"n79054166")

    def test_search_with_special_characters(self):
        viaf_result = self.auth_search.search_viaf_for_lc_id(u"Chopin, Frédéric François (1810-1849)", u"personalNames")
        self.assertEquals(viaf_result, u"n79127769")

        lc_result = self.auth_search.retrieve_lc_name(u"n79127769")
        self.assertEquals(lc_result, u"Chopin, Frédéric, 1810-1849")

    def test_large_search_returns_all_results(self):
        subjects_to_search_for = {(u"geogname", "geogname"),
                                  (u"persname", "persname"),
                                  (u"corpname", "corpname"),
                                  (u"Dickinson, Emily, 1830-1886", "persname"),
                                  (u"Google, Inc.", "corpname"),
                                  (u"Ann Arbor, Mich.", "geogname"),
                                  (u"Chopin, Frédéric François (1810-1849)", "persname")}

        intended_results = {(u'corpname', u'Google, Inc.', u'Google (Firm)', u'http://id.loc.gov/authorities/names/no00095539.html'),
                            (u'geogname', u'Ann Arbor, Mich.', u'Ann Arbor (Mich.)', u'http://id.loc.gov/authorities/names/n79022219.html'),
                            (u'persname', u'Dickinson, Emily, 1830-1886', u'Dickinson, Emily, 1830-1886', u'http://id.loc.gov/authorities/names/n79054166.html'),
                            (u'persname', u"Chopin, Frédéric François (1810-1849)", u"Chopin, Frédéric, 1810-1849", u'http://id.loc.gov/authorities/names/n79127769.html')}

        script_results = self.auth_search.get_lc_authorized_names(subjects_to_search_for)

        self.assertEquals(script_results, intended_results)
