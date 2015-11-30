from unittest import TestCase
from main_projects.aspace_agent_mapping.Famname import Famname


class TestFamname(TestCase):
    def test_get_aspace_json(self):
        name = Famname("Baker family")
        target_json = {"publish": True,
                       "agent_type": "agent_family",
                       "names": [{u"family_name": u"Baker family", u"prefix": u""}, ]}

        self.assertEquals(name.get_aspace_json(), target_json)