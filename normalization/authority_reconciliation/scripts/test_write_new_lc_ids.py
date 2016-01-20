# coding=utf-8
import os
import unittest

from lxml import etree

from write_new_lc_ids import write_new_lc_ids


class TestWritingEADs(unittest.TestCase):

    def test_writing_lc_ids_to_ead(self):
        subjects = [(u'persname', u"Chopin, Frederic 1810-", u"Chopin, Frédéric, 1810-1849", u'http://id.loc.gov/authorities/names/n79127769.html')]
        write_new_lc_ids(subjects, input_directory="../test/subject_write/input", output_directory="../test/subject_write/output")

        tree = etree.parse("../test/subject_write/output/subject_write_test_input.xml")
        persname = tree.xpath("//persname")[0]

        self.assertEquals(persname.text, u"Chopin, Frédéric, 1810-1849")

        os.remove("../test/subject_write/output/subject_write_test_input.xml")