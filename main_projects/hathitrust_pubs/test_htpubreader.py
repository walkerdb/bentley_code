import os
import unittest
from main_projects.hathitrust_pubs.htpubsummarizer import HTPubSummarizer


class TestHTPubSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = HTPubSummarizer(source_file="ht_data.json")

    # def test_loads_from_full_gzip(self):
    #     data = self.reader.load_data_from_ht_gzip_dump(r'C:\Users\wboyle\Downloads\hathi_full_20151101.txt.gz')
    #     self.assertEquals(len(data), 16241)

    def test_loads_from_json(self):
        self.assertEquals(len(self.summarizer.data), 16241)

    def test_groups_by_id(self):
        self.assertEquals(len(self.summarizer.grouped_data), 8071)

    def test_writes_to_file(self):
        self.summarizer._write_data_to_json("ht_write_test.json", {"test": "test"})
        self.assertTrue(os.path.exists("ht_write_test.json"))

    def test_summarizes