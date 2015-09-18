import unittest

from prettifydirectory import extract_list, remove_lists_from_ead


class TestPrettify(unittest.TestCase):
    def setUp(self):
        self.base_input = ['<test>', '<list>text', '  <item>text</item>', '  <list>', '    <item></item>', '  </list>', '</list>', '</test>']
        self.base_output = '<list>text\n  <item>text</item>\n  <list>\n    <item></item>\n  </list>\n</list>'

    def test_extract_list(self):
        i, extracted_list = extract_list(1, self.base_input)
        self.assertEquals(i, 7)
        self.assertEquals(extracted_list, self.base_output)

    def test_remove_lists_from_ead(self):
        text_without_lists, removed_lists = remove_lists_from_ead("test_ead.xml")
        desired_output_text = '<ead>\n' \
                              '  <eadheader>\n' \
                              '    <bioghist>\n' \
                              '      <p>text text text\n' \
                              '$$$$LIST0\n' \
                              '      </p>\n' \
                              '    </bioghist>\n' \
                              '    <scopecontent>\n' \
                              '$$$$LIST1\n' \
                              '    </scopecontent>\n' \
                              '  </eadheader>\n' \
                              '</ead>'
        desired_removed_list = ['        <list>title\n          <item>text\n            <list>text\n              <item></item>\n            </list>\n          </item>\n        </list>', '      <list>text\n        <item></item>\n      </list>']

        self.assertEquals(text_without_lists, desired_output_text)
        self.assertEquals(removed_lists, desired_removed_list)

    def test_remove_long_list(self):
        text_without_lists, removed_lists = remove_lists_from_ead("test_long_ead.xml")
        print(text_without_lists)