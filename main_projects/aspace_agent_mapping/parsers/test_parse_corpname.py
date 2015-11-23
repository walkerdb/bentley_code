# coding=utf-8
import unittest

from parse_corpname import parse_corpname as parse


# agent_corporate_entity: inherits from "abstract_agent"
#                         "names", array
#
# abstract_agent:         "uri": string
#                         "notes": array of note_bioghist objects
#                         "dates_of_existence": array of date objects
#                               "date_type":  "range" or "single"
#                               "label":      "existence"
#                               "expression": the raw text that we want displayed
#                               "begin":      the begin date, YYYY, YYYY-MM, or YYYY-MM-DD
#                               "end":        the end date
#                         "publish": boolean, no default
#
#
# name_corporate_entity:  inherits from "abstract_name"
#                         "primary name": string, required
#                         "subordinate_name_1": string
#                         "subordinate_name_2": string
#                         "number": string
# abstract_name:
#                         "authority_id": string
#                         "dates": string
#                         "use_dates": array of date objects
#                         "qualifier": string
#                         "source": string (enum)
#                         "rules": string (enum)
#                         "authorized": boolean, default false
#                         "is_dislay_name": boolean, default false
#                         "sort_name": string
#                         "sort_name_auto_generate": boolean, default true

class TestParsePersname(unittest.TestCase):
    def setUp(self):
        self.keys = [u"primary_name",
                     u"subordinate_name_1",
                     u"subordinate_name_2",
                     u"qualifier",
                     u"authority_id",
                     u"source",
                     u"date_string",
                     u"auth",
                     u"number",
                     u"date_start",
                     u"date_end"]

    def check_equality(self, output_data, dct):
        for key in self.keys:
            if key not in dct:
                dct[key] = u""

        self.assertEquals(output_data, dct)

    def test_base_case(self):
        parsed = parse("University of Michigan.")
        self.check_equality(parsed, {u"primary_name": u"University of Michigan"})

    def test_qualifier(self):
        parsed = parse("University of Michigan (1940)")
        self.check_equality(parsed, {u"primary_name": u"University of Michigan", u"qualifier": u"1940"})
