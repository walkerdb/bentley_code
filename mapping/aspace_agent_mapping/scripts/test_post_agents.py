import json
from pprint import pprint
from unittest import TestCase

from mapping.aspace_agent_mapping.agent_parsers.Persname import Persname
from mapping.aspace_agent_mapping.agent_parsers.Corpname import Corpname
from mapping.aspace_agent_mapping.agent_parsers.Famname import Famname

from ead_utilities.aspace_interface.pyspace import PySpace


class TestPostAgents(TestCase):
    def setUp(self):
        self.pyspace = PySpace()
        # self.pyspace.delete_all_agents()

    def tearDown(self):
        pass
        # self.pyspace.delete_all_agents()

    def test_post_agent_persname(self):
        test_json = Persname("Superman", "http://id.loc.gov/authorities/names/n2015060724.html", "lcnaf").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "people")
        pprint(test_json)
        pprint(returned_json)

        test_json = Persname("Kent, Clark", "http://id.loc.gov/authorities/names/n2015060724.html", "lcnaf").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "people")
        pprint(test_json)
        pprint(returned_json)

        self.assertEquals(returned_json.get("status", ""), "Created")

    def test_post_corpname(self):
        test_json = Corpname("Johnny Footballs", "https://www.umich.edu/12", "local").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "corporate_entities")
        pprint(test_json)
        pprint(returned_json)

        test_json = Corpname("Jonathan Manziels", "https://www.umich.edu/12", "local").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "corporate_entities")
        pprint(test_json)
        pprint(returned_json)

        self.assertEquals(returned_json.get("status", ""), "Created")

    def test_post_famname(self):
        test_json = Famname("Baker family").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "families")
        self.assertEquals(returned_json.get("status", ""), "Created")

    def test_post_corpname_from_json(self):
        test_json = json.dumps({"names": [{"sort_name_auto_generate": True, "source": "lcnaf", "primary_name": "TEACH Michigan"}], "publish": True})
        returned_json = self.pyspace.add_agent(test_json, "corporate_entities")
        self.assertEquals(returned_json.get("status", ""), "Created")

