from unittest import TestCase
from main_projects.aspace_agent_mapping.Corpname import Corpname
from main_projects.aspace_agent_mapping.Famname import Famname
from main_projects.aspace_agent_mapping.Persname import Persname
from main_projects.aspace_interface.pyspace import PySpace


class TestPostAgents(TestCase):
    def setUp(self):
        self.pyspace = PySpace()
        self.pyspace.delete_all_agents()

    def test_post_agent_persname(self):
        test_json = Persname("Smith, John DM., 1990-2090").get_aspace_json()
        print(self.pyspace.add_agent(test_json, "people"))

    def test_post_corpname(self):
        test_json = Corpname("University of Michigan").get_aspace_json()
        print(self.pyspace.add_agent(test_json, "corporate_entities"))

    def test_post_famname(self):
        test_json = Famname("Baker family").get_aspace_json()
        print(self.pyspace.add_agent(test_json, "families"))
