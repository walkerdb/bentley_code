import unittest
from extents_in_unittitle_parens import EAD

from lxml import etree


class TestEADClass(unittest.TestCase):
    def setUp(self):
        self.ead = EAD()
        self.ead.set_path("ead.xml")

    def test_class_setup(self):
        ead = EAD()
        ead.set_path("ead.xml")
        self.assertEquals(ead.path_to_ead, "ead.xml")

    def test_etree_creation(self):
        self.ead.make_tree()

        print(self.ead.path_to_ead)
        self.assertEquals(self.ead.tree, etree.parse("ead.xml"))
