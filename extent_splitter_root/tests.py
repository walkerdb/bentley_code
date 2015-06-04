# coding=utf-8
import unittest
from extent_parser import split_extents


class TestExtentSplitter(unittest.TestCase):
    def check_output_equality(self, original_text, target_list):
        split_extent = split_extents(original_text)
        self.assertEqual(split_extent, target_list)

    # Extent statements should be split by " and "
    def test_split_first_two_element_extent_string(self):
        self.check_output_equality("4 linear feet and 1 oversize volume", ["4 linear feet", "1 oversize volume"])

    # Extent statements should be split by commas
    def test_split_extent_with_commas(self):
        self.check_output_equality(
            "3 linear feet, 1 oversize volume, and 5 motion picture reels",
            ["3 linear feet", "1 oversize volume", "5 motion picture reels"]
        )

    # Ensure trailing whitespace is removed
    def test_whitespace_removal(self):
        self.check_output_equality("4 linear feet ", ["4 linear feet"])

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
            ["1 photograph", "15 hairpins", "25 quarks"]
        )

    # extra whitespace and all newlines should be removed
    def test_remove_extra_whitespace_and_newlines(self):
        self.check_output_equality("1 why did they ever\n\n             do this?", ["1 why did they ever do this?"])

    # replace contractions with spelled-out version
    def test_contraction_expansion(self):
        self.check_output_equality("12 linear ft., 12 5-in. doilies", ["12 linear feet", "12 5-inch doilies"])

    # special case for inch pluralization and reels
    def test_reel_inch_expansion_and_pluralization(self):
        self.check_output_equality("27 1/4 in. reels", ["27 1/4-inch reels"])

    # when "and" appears in a paren, do not split it
    def test_no_split_and_in_paren(self):
        self.check_output_equality(
            "12 Beowulfs (in 1 Hwæt! and 2 battles), 1 þæt wæs god cyning",
            ["12 Beowulfs (in 1 Hwæt! and 2 battles)", "1 þæt wæs god cyning"]
        )

    def test_ips_dont_become_own_statement(self):
        self.check_output_equality("1 7-inch reel, 7 3/4 ips", ["1 7-inch reel, 7 3/4 ips"])
        self.check_output_equality("1 nothing important, 1 7-inch reel 7 3/4 ips", ["1 nothing important", "1 7-inch reel 7 3/4 ips"])

if __name__ == "__main__":
    unittest.main()