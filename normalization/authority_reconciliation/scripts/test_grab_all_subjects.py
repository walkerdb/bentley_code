from pprint import pprint
import unittest
from lxml import etree
from grab_all_subjects import grab_all_subjects_from_etree, grab_all_subjects

class TestGrabAllSubjects(unittest.TestCase):
    def setUp(self):
        self.test_ead = r"..\test\subject_grab\subject_grab_test_ead_1.xml"
        self.test_directory = r"..\test\subject_grab"
        self.tree = etree.parse(self.test_ead)

    def test_extract_from_single_ead(self):
        subjects = grab_all_subjects_from_etree(self.tree)
        subject_tuple = (u'controlaccess persname [ca2]', 'persname')
        self.assertTrue(subject_tuple in subjects)

    def test_extract_from_multiple_ead(self):
        subjects = grab_all_subjects(self.test_directory)

        subject_from_ead_one = (u'corpname from ead 1', 'corpname')
        subject_from_ead_two = (u'corpname from ead 2', 'corpname')

        self.assertTrue(subject_from_ead_one in subjects)
        self.assertTrue(subject_from_ead_two in subjects)
