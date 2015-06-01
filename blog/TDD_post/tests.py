import unittest
from extent_splitter import split_extents


class TestExtentSplitter(unittest.TestCase):

    def setUp(self):
        self.basic_extent = "4 linear feet and 1 oversize volume"
        self.basic_extent_target_output = ["4 linear feet", "1 oversize volume"]
        self.extent_with_commas_raw_text = "3 linear ft., 1 oversize volume, and 5 motion picture reels"
        self.extent_with_commas_target_output = ["3 linear ft.", "1 oversize volume", "5 motion picture reels"]
        self.extent_in_parentheses = "3 linear ft., 1 oversize volume, and 5 motion picture reels (in 4 boxes)"
        self.extent_in_parentheses_target_output = ["3 linear ft.", "1 oversize volume", "5 motion picture reels", "(in 4 boxes)"]
        self.extent_in_brackets = "256 MB [150 diskettes]"
        self.extent_in_brackets_target_output = ["256 MB", "[150 diskettes]"]
        self.extent_with_in_raw_text = "26 linear feet in 27 boxes"
        self.extent_with_in_target_output = ["26 linear feet", "27 boxes"]
        self.extent_with_whitespace = "4 linear feet "
        self.extent_with_whitespace_target_output = ["4 linear feet"]

    # Helper function for tests - saves extra lines of code
    def check_extent_equality(self, original_text, target_list):
        split_extent = split_extents(original_text)
        self.assertEqual(split_extent, target_list)

    # Extent statements should be split by " and "
    def test_split_first_two_element_extent_string(self):
        self.check_extent_equality(
            self.basic_extent,
            self.basic_extent_target_output)

    # Extent statements should be split by commas
    def test_split_extent_with_commas(self):
        self.check_extent_equality(
            self.extent_with_commas_raw_text,
            self.extent_with_commas_target_output)

    # When there is a parenthetical extent, this should
    # be split off as well, but should retain parentheses
    def test_split_parenthetical_extent(self):
        self.check_extent_equality(
            self.extent_in_parentheses,
            self.extent_in_parentheses_target_output)

    # Same with extents in brackets
    def test_split_bracketed_extent(self):
        self.check_extent_equality(
            self.extent_in_brackets,
            self.extent_in_brackets_target_output)

    # Ensure trailing whitespace is removed
    def test_whitespace_removal(self):
        self.check_extent_equality(
            self.extent_with_whitespace,
            self.extent_with_whitespace_target_output)

    # Ensure extents are also split by the " in " keyword
    def test_split_extent_by_in(self):
        self.check_extent_equality(
            self.extent_with_in_raw_text,
            self.extent_with_in_target_output)



if __name__ == "__main__":
    unittest.main()