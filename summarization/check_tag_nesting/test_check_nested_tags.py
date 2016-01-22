import unittest

from ead_utilities.ead_utilities import EAD
from summarization.check_tag_nesting.check_nested_tags import find_nested_tags

class TestCheckNestedTags(unittest.TestCase):
    def setUp(self):
        self.positive_test_case_loc = "positive_case_ead.xml"
        self.negative_test_case_loc = "negative_case_ead.xml"

    def test_positive_match(self):
        ead = EAD(filepath=self.positive_test_case_loc)
        self.assertEquals(find_nested_tags(ead), [['positive_case_ead.xml', '/unittitle', 'unittitle']])

    def test_negative_match(self):
        ead = EAD(filepath=self.negative_test_case_loc)
        self.assertEquals(find_nested_tags(ead), [])
