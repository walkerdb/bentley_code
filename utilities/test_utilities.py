import os
import unittest

from lxml import etree

from utilities import EAD, EADDir


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

class TestApplicator(unittest.TestCase):
    def setUp(self):
        self.a = EADDir(input_dir=r'C:\Users\wboyle\PycharmProjects\bentley_code\utilities')

    def _method_for_testing_write(self, ead):
        texts = ead.tree.xpath("//text")
        for text in texts:
            text.text = "yo"

    def _method_for_testing_characterize(self, ead):
        results = []
        texts = ead.tree.xpath("//text")
        for text in texts:
            results.append(text.text)
        return results

    def test_ead_list(self):
        self.assertEquals(self.a.ead_files, ['ead_appended.xml', 'ead_messy.xml', 'ead_pretty.xml'])

    def test_characterize_directory(self):
        intended_results = [['text'], ['text'], ['text']]
        self.assertEquals(self.a.characterize_dir(function=self._method_for_testing_characterize), intended_results)

    def test_apply_to_directory(self):
        output_dir = os.path.join(self.a.input_dir, "output")
        self.a.apply_function_to_dir(function=self._method_for_testing_write, output_dir=output_dir)

        b = EADDir(output_dir)
        intended_results = [['yo'], ['yo'], ['yo']]
        self.assertEquals(b.characterize_dir(self._method_for_testing_characterize), intended_results)

        for ead in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, ead))
