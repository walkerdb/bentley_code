import json
from pprint import pprint
from unittest import TestCase

from mapping.aspace_agent_mapping.agent_parsers.Persname import Persname
from mapping.aspace_agent_mapping.agent_parsers.Corpname import Corpname
from mapping.aspace_agent_mapping.agent_parsers.Famname import Famname
from mapping.aspace_agent_mapping.scripts.post_agents import extract_aspace_id

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

    def test_multiple_with_same_auth_id_returns_correct_conflicting_record_id(self):
        test_json1 = Corpname("asldkajsdklasj", "https://www.definitelyunique.com", "local").get_aspace_json()
        test_json2 = Corpname("lksjdflksjlks", "https://www.definitelyunique.com", "local").get_aspace_json()

        returned_json_1 = self.pyspace.add_corporation(test_json1)
        returned_json_2 = self.pyspace.add_corporation(test_json2)

        id_1 = extract_aspace_id(json.loads(test_json1), returned_json_1, self.pyspace)
        id_2 = extract_aspace_id(json.loads(test_json2), returned_json_2, self.pyspace)

        self.agent_uris.append(id_1)
        self.agent_uris.append(id_2)

        self.assertEquals(id_1, id_2)
