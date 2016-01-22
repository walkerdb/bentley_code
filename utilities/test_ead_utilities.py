import os
import unittest

from lxml import etree

from ead_utilities import EAD, EADDir


class TestEADClass(unittest.TestCase):
    def setUp(self):
        self.ead = EAD(filepath=r"test_files\ead_messy.xml")
        self.test_output_dir = r"test_files\output"

    def test_filename(self):
        self.assertEquals(self.ead.filename, r"ead_messy.xml")

    def test_etree_creation(self):
        self.assertEquals(etree.tostring(self.ead.tree), etree.tostring(etree.parse(r"test_files\ead_messy.xml")))

    def test_pretty_printing(self):
        self.ead.prettyprint(output_dir=self.test_output_dir)
        with open(os.path.join(self.test_output_dir, self.ead.filename)) as f:
            ead_prettyprinted = f.read()

        with open(r"test_files\ead_pretty.xml") as f:
            ideal_output = f.read()

        self.assertEquals(ead_prettyprinted, ideal_output)

        os.remove(os.path.join(self.test_output_dir, self.ead.filename))

    def test_edit_and_output(self):
        new_node = etree.Element("new_node")
        new_node.text = "new text"

        self.ead.tree.xpath("/ead")[0].append(new_node)
        self.ead.prettyprint(output_dir=self.test_output_dir)

        with open(os.path.join(self.test_output_dir, self.ead.filename)) as f:
            ead_prettyprinted = f.read()

        with open(r"test_files\ead_appended.xml") as f:
            ideal_output = f.read()

        self.assertEquals(ead_prettyprinted, ideal_output)

class TestApplicator(unittest.TestCase):
    def setUp(self):
        self.a = EADDir(input_dir=r'test_files')
        self.test_output_dir = r"test_files\output"

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
        self.a.apply_function_to_dir(function=self._method_for_testing_write, output_dir=self.test_output_dir)

        b = EADDir(self.test_output_dir)
        intended_results = [['yo'], ['yo'], ['yo']]
        self.assertEquals(b.characterize_dir(self._method_for_testing_characterize), intended_results)

        for ead in os.listdir(self.test_output_dir):
            os.remove(os.path.join(self.test_output_dir, ead))
