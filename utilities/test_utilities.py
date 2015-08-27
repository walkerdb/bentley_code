import os
import unittest
import contextlib

from lxml import etree

from utilities import EAD


class TestEADClass(unittest.TestCase):
    def setUp(self):
        self.ead = EAD(filepath="ead_messy.xml")

    def test_filename(self):
        self.assertEquals(self.ead.filename, "ead_messy.xml")

    def test_etree_creation(self):
        self.assertEquals(etree.tostring(self.ead.tree), etree.tostring(etree.parse("ead_messy.xml")))

    def test_pretty_printing(self):
        output_dir = "output"
        self.ead.prettyprint(output_dir=output_dir)
        with open(os.path.join(output_dir, self.ead.filename)) as f:
            ead_prettyprinted = f.read()

        with open("ead_pretty.xml") as f:
            ideal_output = f.read()

        self.assertEquals(ead_prettyprinted, ideal_output)

        os.remove(os.path.join(output_dir, self.ead.filename))

    def test_edit_and_output(self):
        new_node = etree.Element("new_node")
        new_node.text = "new text"

        self.ead.tree.xpath("/ead")[0].append(new_node)
        self.ead.prettyprint(output_dir="output")

        with open(os.path.join("output", self.ead.filename)) as f:
            ead_prettyprinted = f.read()

        with open("ead_appended.xml") as f:
            ideal_output = f.read()

        self.assertEquals(ead_prettyprinted, ideal_output)
