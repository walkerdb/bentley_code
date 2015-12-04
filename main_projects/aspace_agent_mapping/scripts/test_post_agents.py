from unittest import TestCase
import json

from main_projects.aspace_agent_mapping.agent_parsers.Corpname import Corpname
from main_projects.aspace_agent_mapping.agent_parsers.Famname import Famname
from main_projects.aspace_agent_mapping.agent_parsers.Persname import Persname
from main_projects.aspace_interface.pyspace import PySpace


class TestPostAgents(TestCase):
    def setUp(self):
        self.pyspace = PySpace()
        self.pyspace.delete_all_agents()

    def tearDown(self):
        self.pyspace.delete_all_agents()

    def test_post_agent_persname(self):
        test_json = Persname("Smith, John DM.").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "people")
        print(returned_json)
        self.assertEquals(returned_json.get("status", ""), "Created")

    def test_post_corpname(self):
        test_json = Corpname("University of Michigan").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "corporate_entities")
        self.assertEquals(returned_json.get("status", ""), "Created")

    def test_post_famname(self):
        test_json = Famname("Baker family").get_aspace_json()
        returned_json = self.pyspace.add_agent(test_json, "families")
        self.assertEquals(returned_json.get("status", ""), "Created")

    def test_post_corpname_from_json(self):
        test_json = json.dumps({"names": [{"sort_name_auto_generate": True, "source": "lcnaf", "primary_name": "TEACH Michigan"}], "publish": True})
        returned_json = self.pyspace.add_agent(test_json, "corporate_entities")
        self.assertEquals(returned_json.get("status", ""), "Created")

