from unittest import TestCase
from main_projects.aspace_agent_mapping.Corpname import Corpname


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

    def add_empty_fields(self, dct):
        for key in self.keys:
            if key not in dct:
                dct[key] = u""
        return dct

    def test_get_json(self):
        name = Corpname("test corpname")
        output_json = name.get_aspace_json()
        target_json = {"publish": True, "agent_type": "agent_corporate_entity", "names": [self.add_empty_fields({u"primary_name": u"test corpname"})]}

        self.assertEquals(output_json, target_json)
