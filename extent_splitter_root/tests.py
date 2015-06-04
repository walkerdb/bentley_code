import unittest
from extent_splitter_root import split_extents


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
    def check_output_equality(self, original_text, target_list):
        split_extent = split_extents(original_text)
        self.assertEqual(split_extent, target_list)

    # Extent statements should be split by " and "
    def test_split_first_two_element_extent_string(self):
        self.check_output_equality(self.basic_extent, self.basic_extent_target_output)

    # Extent statements should be split by commas
    def test_split_extent_with_commas(self):
        self.check_output_equality(self.extent_with_commas_raw_text, self.extent_with_commas_target_output)

    # When there is a parenthetical extent, this should
    # be split off as well, but should retain parentheses
    def test_split_parenthetical_extent(self):
        self.check_output_equality(self.extent_in_parentheses, self.extent_in_parentheses_target_output)

    # Same with extents in brackets
    def test_split_bracketed_extent(self):
        self.check_output_equality(self.extent_in_brackets, self.extent_in_brackets_target_output)

    # Ensure trailing whitespace is removed
    def test_whitespace_removal(self):
        self.check_output_equality(self.extent_with_whitespace, self.extent_with_whitespace_target_output)

    # Ensure extents are also split by the " in " keyword
    def test_split_extent_by_in(self):
        self.check_output_equality(self.extent_with_in_raw_text, self.extent_with_in_target_output)

    # "black and white" should not be split
    def test_no_split_black_and_white(self):
        self.check_output_equality("black and white", ["black and white"])

    # if there are no numbers in a paren, don't split it off
    def test_no_split_paren_with_no_numbers(self):
        self.check_output_equality("1 whats-it (sparkly)", ["1 whats-it (sparkly)"])

    # if there are no numbers in general in an element, don't split it
    def test_no_split_extent_with_no_numbers(self):
        self.check_output_equality("25 thing-a-ma-bobs, galore", ["25 thing-a-ma-bobs, galore"])

    # if the first element has no numbers, don't remove
    def test_no_number_first_element_recovery(self):
        self.check_output_equality("nothing, 25 somethings", ["nothing", "25 somethings"])

    # written-out numbers should be replaced
    def test_replace_written_out_numbers(self):
        self.check_output_equality(
            "one photograph, fifteen hairpins, Twenty-five quarks",
            ["1 photograph", "15 hairpins", "25 quarks"])

    # extra whitespace and all newlines should be removed
    def test_remove_extra_whitespace_and_newlines(self):
        self.check_output_equality("1 why did they ever\n\n             do this?", ["1 why did they ever do this?"])


if __name__ == "__main__":
    unittest.main()