from unittest import TestCase

from main_projects.aspace_agent_mapping.Persname import Persname


class TestPersname(TestCase):
    def setUp(self):
        self.keys = [u"primary_name", u"title", u"name_order", u"prefix", u"rest_of_name", u"suffix", u"fuller_form",
                     u"number"]

    def add_empty_fields(self, dct):
        for key in self.keys:
            if key not in dct:
                dct[key] = u""
        return dct

    def test_get_aspace_json(self):
        name = Persname("John Smith, 1980-2090")
        date_json = {"date_type": "range", "label": "existence", "expression": u"1980-2090", "begin": u"1980", "end": u"2090"}
        target_json = {"publish": True,
                       "agent_type": "agent_person",
                       "dates_of_existence": [date_json, ],
                       "names": [self.add_empty_fields({u"primary_name": u"Smith", u"rest_of_name": u"John"}), ]}

        self.assertEquals(name.get_aspace_json(), target_json)
