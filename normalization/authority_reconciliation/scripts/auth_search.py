import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


class AuthoritySearcher(object):
    def __init__(self):
        self.subject_type_to_search_type_map = {u"geogname": u"geographicNames",
                                                u"persname": u"personalNames",
                                                u"corpname": u"corporateNames"}

        self.viaf_search_template = u'http://viaf.org/viaf/search/viaf?query=local.{0}+all+"{1}"+and+local.sources+any+"lc"&sortKeys=holdingscount&httpAccept=application/xml'
        self.lc_auth_template = u"http://id.loc.gov/authorities/names/{0}.html"
        self.headers = {"user-agent": "Bentley Historical Library authority reconciliation bot v.1.0"}


    def get_lc_authorized_names(self, subjects):
        results = set()

        for subject in tqdm(subjects, desc="Searching VIAF for LoC identifiers, then LoC for authorized names..."):
            time.sleep(2)
            subject_text, subject_type = subject
            search_type = self.subject_type_to_search_type_map[subject_type]

            lc_id = self.search_viaf_for_lc_id(search_term=subject_text, search_type=search_type)

            if not lc_id:
                continue

            auth_name = self.retrieve_lc_name(lc_id)
            lc_address = self.lc_auth_template.format(lc_id)

            results.add((subject_type, subject_text, auth_name, lc_address))


        return results


    def search_viaf_for_lc_id(self, search_term, search_type):
        query = self._create_viaf_query(search_term=search_term, search_type=search_type)

        return self._get_lc_id_from_viaf_results(requests.get(query, headers=self.headers).content)


    def retrieve_lc_name(self, lc_auth_id):
        query = self.lc_auth_template.format(lc_auth_id)
        response = requests.get(query, headers=self.headers).text
        soup = BeautifulSoup(response, "lxml")
        return unicode(soup.h1.text)


    def _create_viaf_query(self, search_term, search_type):
        return self.viaf_search_template.format(search_type, search_term)


    @staticmethod
    def _get_lc_id_from_viaf_results(viaf_xml_response):
        tree = etree.fromstring(viaf_xml_response)
        results = tree.xpath("//*[local-name()='record']")

        if not results:
            return ""

        primary_result = results[0]
        sources = primary_result.xpath("//*[local-name()='mainHeadingEl']/*[local-name()='id']")

        if not sources:
            return ""

        lc_identifier = ""
        for source in sources:
            if "LC|" in source.text:
                lc_identifier = source.text.split("|")[1].replace(" ", "")
                break

        if not lc_identifier:
            return ""

        return unicode(lc_identifier)

