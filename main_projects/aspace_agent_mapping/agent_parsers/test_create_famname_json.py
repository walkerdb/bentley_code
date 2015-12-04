import unittest

from main_projects.aspace_agent_mapping.agent_parsers.create_famname_json import parse_famname as parse

class TestFamnameParser(unittest.TestCase):

    def test_name_parsed(self):
        parsed = parse("Baker family")
        self.assertEquals(parsed, {u"family_name": u"Baker family", u"source": u"local", u"sort_name_auto_generate": True})
