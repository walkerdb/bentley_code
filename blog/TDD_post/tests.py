import unittest

from blog.TDD_post.extent_splitter import split_extents


class TestExtentSplitter(unittest.TestCase):

    def setUp(self):
        self.extent_1_raw_text = "4 linear feet and 1 oversize volume"
        self.extent_1_target_output = ["4 linear feet", "1 oversize volume"]
        self.extent_2_raw_text = "1 oversize volume and 5 motion picture reels"
        self.extent_2_target_output = ["1 oversize volume", "5 motion picture reels"]
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

    def test_split_first_two_element_extent_string(self):
        split_extent = split_extents(self.extent_1_raw_text)
        self.assertEquals(split_extent, self.extent_1_target_output)

    def test_split_second_two_element_extent_string(self):
        split_extent = split_extents(self.extent_2_raw_text)
        self.assertEquals(split_extent, self.extent_2_target_output)

    def test_split_extent_with_commas(self):
        split_extent = split_extents(self.extent_with_commas_raw_text)
        self.assertEquals(split_extent, self.extent_with_commas_target_output)

    # When there is a parenthetical extent, this should be split off as well, but should retain parentheses
    def test_split_parenthetical_extent(self):
        split_extent = split_extents(self.extent_in_parentheses)
        self.assertEquals(split_extent, self.extent_in_parentheses_target_output)

    # Same with extents in brackets
    def test_split_bracketed_extent(self):
        split_extent = split_extents(self.extent_in_brackets)
        self.assertEquals(split_extent, self.extent_in_brackets_target_output)

    # Ensure trailing whitespace is removed
    def test_whitespace_removal(self):
        split_extent = split_extents(self.extent_with_whitespace)
        self.assertEquals(split_extent, self.extent_with_whitespace_target_output)

    # Ensure extents are also split by the " in " keyword
    def test_split_extent_by_in(self):
        split_extent = split_extents(self.extent_with_in_raw_text)
        self.assertEquals(split_extent, self.extent_with_in_target_output)


if __name__ == "__main__":
    unittest.main()