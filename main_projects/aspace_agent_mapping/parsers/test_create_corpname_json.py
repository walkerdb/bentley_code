# coding=utf-8
import unittest

from create_corpname_json import parse_corpname as parse


# agent_corporate_entity: inherits from "abstract_agent"
#                         "names", array of name_corporate_entity objects
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
# {publish: true, names: [{primary_name: "", subordinate_name_1: "", subordinate_name_2: "", authority_id: "", source: "", qualifier: ""}]
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
                     u"number",
                     u"date_start",
                     u"date_end"]

    def check_equality(self, output_data, dct):
        for key in self.keys:
            if key not in dct:
                dct[key] = u""

        self.assertEquals(output_data, dct)

    def test_should_return_a_primary_name(self):
        parsed = parse("University of Michigan.")
        self.check_equality(parsed, {u"primary_name": u"University of Michigan"})

    def test_should_extract_qualifiers(self):
        parsed = parse("University of Michigan (1940)")
        self.check_equality(parsed, {u"primary_name": u"University of Michigan", u"qualifier": u"1940"})

        parsed = parse("University of (parenthetical) Michigan (1939)")
        self.check_equality(parsed, {u"primary_name": u"University of (parenthetical) Michigan", u"qualifier": u"1939"})

    def test_string_with_two_entities_should_split_accordingly(self):
        parsed = parse("University of Michigan. School of Education.")
        self.check_equality(parsed, {u"primary_name": u"University of Michigan", u"subordinate_name_1": u"School of Education"})

    def test_string_with_three_entities_should_split_accordingly(self):
        parsed = parse("United States. Army. Michigan Cavalry Regiment, 3rd (1861-1866)")
        self.check_equality(parsed, {u"primary_name": u"United States", u"subordinate_name_1": u"Army", u"subordinate_name_2": u"Michigan Cavalry Regiment, 3rd", u"qualifier": u"1861-1866"})

    def test_excess_sub_parts_should_all_go_in_part_2(self):
        parsed = parse("United States. Army. Navy. Michigan Cavalry Regiment, 3rd (1861-1866)")
        self.check_equality(parsed, {u"primary_name": u"United States", u"subordinate_name_1": u"Army", u"subordinate_name_2": u"Navy. Michigan Cavalry Regiment, 3rd", u"qualifier": u"1861-1866"})

    def test_periods_that_are_not_signifying_end_of_entity_are_ignored(self):
        names = ["Huron-Arbor Temple no. 66", "Lickly Corners Grange, no. 274", "Essanay Film Manufacturing Co. films", "St. Stephen's Episcopal Church", "Remington Rand, inc. foods"]
        for name in names:
            self.check_equality(parse(name), {u"primary_name": unicode(name)})

    def test_auth_id_and_source_should_be_included(self):
        parsed = parse("test corpname", "www.loc.gov", "lcnaf")
        self.check_equality(parsed, {u"primary_name": u"test corpname", u"authority_id": u"www.loc.gov", u"source": u"lcnaf"})

