import json
from pprint import pprint
from unittest import TestCase

from mapping.aspace_agent_mapping.agent_parsers.Persname import Persname
from mapping.aspace_agent_mapping.agent_parsers.Corpname import Corpname
from mapping.aspace_agent_mapping.agent_parsers.Famname import Famname

from utilities.aspace_interface.pyspace import PySpace


class TestPostAgents(TestCase):
    def setUp(self):
        self.pyspace = PySpace()
        self.agent_uris = []

    def tearDown(self):
        for uri in self.agent_uris:
            self.pyspace.delete_agent_by_uri(uri)

    def test_post_agent_persname(self):
        test_json = Persname("Walker", "http://www.walkerdb.com", "lcnaf").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "people")

        self.assertEquals(returned_json.get("status", ""), "Created")
        self.agent_uris.append(returned_json[u'uri'])

    def test_post_corpname(self):
        test_json = Corpname("Skynet Inc.", "https://www.totallyharmless.com", "local").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "corporate_entities")

        self.assertEquals(returned_json.get("status", ""), "Created")
        self.agent_uris.append(returned_json[u'uri'])

    def test_post_famname(self):
        test_json = Famname("Boyle family").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "families")

        self.assertEquals(returned_json.get("status", ""), "Created")
        self.agent_uris.append(returned_json[u'uri'])
