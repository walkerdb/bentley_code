from unittest import TestCase
import json

from mapping.aspace_agent_mapping.agent_parsers.Famname import Famname


class TestFamname(TestCase):
    def test_get_aspace_json(self):
        test_json = json.loads(Famname("Baker family").get_aspace_json())
        target_json = {u"publish": True,
                       u"names": [{u"family_name": u"Baker family", u"source": u"local", u"sort_name_auto_generate": True}, ]}

        self.assertEquals(test_json, target_json)