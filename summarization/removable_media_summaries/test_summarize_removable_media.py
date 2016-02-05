import unittest
import summarize_removable_media as srm


class TestSummarizeRemovableMedia(unittest.TestCase):
    def testLocationDiscovery(self):
        self.assertEquals(srm.get_location("87207", "box", "21"), "Y-624-K")
