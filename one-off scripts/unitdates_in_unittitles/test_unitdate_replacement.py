import unittest

from lxml import etree

from find_prime_suspects import move_unitdates as mu

class TestUnitdateReplacement(unittest.TestCase):
	def test_base_case(self):
		unittitle_input = etree.fromstring("<parent><unittitle>text <unitdate>3000</unitdate> more text <corpname>corp</corpname></unittitle><sibling>b</sibling></parent>")
		unittitle_input = unittitle_input.xpath("unittitle")[0]
		unittitle_target = etree.fromstring("<parent><unittitle>text 3000 more text <corpname>corp</corpname></unittitle><unitdate>3000</unitdate><sibling>b</sibling></parent>")
		self.assertEquals(etree.tostring(mu(unittitle_input).getparent()), etree.tostring(unittitle_target))