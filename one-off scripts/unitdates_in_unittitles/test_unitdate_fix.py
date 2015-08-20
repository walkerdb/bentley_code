import unittest

from lxml import etree

from unitdates_unittitles_fix import move_unitdates
from unitdates_unittitles_fix import determine_action


class TestUnitdateReplacement(unittest.TestCase):
	def test_calcify_base_case(self):
		unittitle_input = etree.fromstring("<parent><unittitle>text <unitdate>3000</unitdate> more text</unittitle><sibling>b</sibling></parent>")
		unittitle_input = unittitle_input.xpath("unittitle")[0]
		unittitle_target = etree.fromstring("<parent><unittitle>text 3000 more text</unittitle><unitdate>3000</unitdate><sibling>b</sibling></parent>")
		self.assertEquals(etree.tostring(move_unitdates(unittitle_input, "move_and_calcify").getparent()), etree.tostring(unittitle_target))

	def test_calcify_with_extra_tags(self):
		unittitle_input = etree.fromstring("<parent><unittitle>text <unitdate>3000</unitdate> more text <corpname>corp</corpname></unittitle><sibling>b</sibling></parent>")
		unittitle_input = unittitle_input.xpath("unittitle")[0]
		unittitle_target = etree.fromstring("<parent><unittitle>text 3000 more text <corpname>corp</corpname></unittitle><unitdate>3000</unitdate><sibling>b</sibling></parent>")
		self.assertEquals(etree.tostring(move_unitdates(unittitle_input, "move_and_calcify").getparent()), etree.tostring(unittitle_target))

	def test_clean_base_case(self):
		ut_input = etree.fromstring("<parent><unittitle>text <unitdate>3000</unitdate>, <unitdate>4000</unitdate>, and <unitdate>900</unitdate></unittitle></parent>")
		ut_input = ut_input.xpath("unittitle")[0]
		ut_target = etree.fromstring("<parent><unittitle>text</unittitle><unitdate>3000</unitdate><unitdate>4000</unitdate><unitdate>900</unitdate></parent>")
		self.assertEquals(etree.tostring(move_unitdates(ut_input, "move_and_clean").getparent()), etree.tostring(ut_target))


class TestDetermineAction(unittest.TestCase):
	def test_calcify_base(self):
		ut_input = etree.fromstring("{0}text {1}1945{2} now more text {1}1956{2}{3}".format("<unittitle>", "<unitdate>", "</unitdate>", "</unittitle>"))
		self.assertEquals(determine_action(ut_input), "move_and_calcify")

	def test_clean_base(self):
		ut_input = etree.fromstring("{0}text {1}1945{2}, {1}1956{2}, and {1}1920{2}{3}".format("<unittitle>", "<unitdate>", "</unitdate>", "</unittitle>"))
		self.assertEquals(determine_action(ut_input), "move_and_clean")

	def test_null_case(self):
		ut_input = etree.fromstring("{0}text {1}1945{2}{3}".format("<unittitle>", "<unitdate>", "</unitdate>", "</unittitle>"))
		self.assertEquals(determine_action(ut_input), "")

	def test_clean_base_false_positive(self):
		ut_input = etree.fromstring("{0}text {1}1945{2}, {1}1956{2}, also {1}1920{2}{3}".format("<unittitle>", "<unitdate>", "</unitdate>", "</unittitle>"))
		self.assertEquals(determine_action(ut_input), "")
