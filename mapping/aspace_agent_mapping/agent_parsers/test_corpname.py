from unittest import TestCase
import json

from mapping.aspace_agent_mapping.agent_parsers.Corpname import Corpname


class TestCorpname(TestCase):
    def setUp(self):
        self.keys = [u"primary_name",
                     u"subordinate_name_1",
                     u"subordinate_name_2",
                     u"qualifier",
                     u"authority_id",
                     u"source",
                     u"date_string",
                     u"number",
                     u"date_start",
                     u"date_end"]

    def test_get_json(self):
        name = Corpname("test corpname")
        output_json = json.loads(name.get_aspace_json())
        target_json = {u"publish": True, u"names": [{u"primary_name": u"test corpname", u"sort_name_auto_generate": True}]}

        self.assertEquals(output_json, target_json)
