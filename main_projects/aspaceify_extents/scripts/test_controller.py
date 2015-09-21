import unittest

from lxml import etree

from controller import split_extents
from utilities import utilities as utils

class TestController(unittest.TestCase):
    def setUp(self):
        self.test_input = utils.EAD("test_ead.xml")

    def test_base_case(self):
        desired_output = utils.EAD("test_ead_desired.xml")
        self.assertEquals(etree.tostring(split_extents(self.test_input).tree).replace("\n", "").replace(" ", ""), etree.tostring(desired_output.tree).replace("\n", "").replace(" ", ""))
