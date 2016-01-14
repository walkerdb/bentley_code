from unittest import TestCase
import json

from mapping.aspace_agent_mapping.agent_parsers import Persname


class TestPersname(TestCase):
    def setUp(self):
        self.keys = [u"primary_name", u"title", u"name_order", u"prefix", u"rest_of_name", u"suffix", u"fuller_form",
                     u"number"]

    def test_get_aspace_json(self):
        test_json = json.loads(Persname("John Smith, 1980-2090").get_aspace_json())
        date_json = {u"date_type": u"range", u"label": u"existence", u"expression": u"1980-2090", u"begin": u"1980", u"end": u"2090"}
        target_json = {u"publish": True,
                       u"dates_of_existence": [date_json, ],
                       u"names": [{u"primary_name": u"Smith", u"rest_of_name": u"John", u"name_order": u"inverted", u"sort_name_auto_generate": True}, ]}

        self.assertEquals(test_json, target_json)
