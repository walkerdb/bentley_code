# coding=utf-8
from __future__ import absolute_import
import unittest

from aspaceify_extents.scripts.extent_parser import split_into_extents


class TestExtentSplitter(unittest.TestCase):
    def check_output_equality(self, original_text, target_list):
        split_extent = split_into_extents(original_text)
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
    def test_dont_split_black_and_white(self):
        self.check_output_equality("black and white", ["black and white"])

    # if there are no numbers in a paren, don't split it off
    def test_dont_split_paren_with_no_numbers(self):
        self.check_output_equality("1 whats-it (sparkly)", ["1 whats-it (sparkly)"])

    # if there are no numbers in general in an element, don't split it
    def test_dont_split_extent_containing_zero_numbers(self):
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
        self.check_output_equality("12 outsize boxes", ["12 oversize boxes"])
        self.check_output_equality("2 col. maps", ["2 color maps"])
        self.check_output_equality("7-in. reel", ["7-inch reel"])

    # special case for inch pluralization and reels
    def test_reel_inch_expansion_and_pluralization(self):
        self.check_output_equality("27 1/4 in. reels", ["27 1/4-inch reels"])

    # when "and" appears in a paren, do not split it
    def test_dont_split_by_and_when_and_in_paren(self):
        self.check_output_equality(
            "12 Beowulfs (in 1 Hwaet! and 2 battles), 1 thaet waes god cyning",
            ["12 Beowulfs (in 1 Hwaet! and 2 battles)", "1 thaet waes god cyning"]
        )

    def test_and_in_parens_edge_case_success(self):
        self.check_output_equality(
            "1.5 linear feet (in 2 boxes) and 30.9 GB (online)",
            ["1.5 linear feet (in 2 boxes)", "30.9 GB (online)"]
        )

    def test_ips_dont_become_own_statement(self):
        self.check_output_equality("1 7-inch reel, 7 3/4 ips", ["1 7-inch reel, 7 3/4 ips"])
        self.check_output_equality(
            "1 nothing important, 1 7-inch reel 7 3/4 ips",
            ["1 nothing important", "1 7-inch reel 7 3/4 ips"]
        )

    def test_wonky_audio_string_remains_unchanged(self):
        self.check_output_equality(
            "5 floppy sound discs, 7 1/2 in., 33 1/3 rpm",
            ["5 floppy sound discs, 7 1/2 inches, 33 1/3 rpm"]
        )

    def test_numbers_with_commas_fully_reconstruct(self):
        self.check_output_equality("1,900 floppy disks, 50 dementors", ["1,900 floppy disks", "50 dementors"])

    def test_dimension_clauses_dont_return_split(self):
        self.check_output_equality(
            "3 sheets : various media ; 43.3 x 56.1 cm. (17-1/8 x 22-1/8 in.) or smaller.",
            ["3 sheets : various media ; 43.3 x 56.1 cm. (17-1/8 x 22-1/8 inches) or smaller."]
        )

    def test_no_doesnt_return_split(self):
        self.check_output_equality(
            "2 folders and 3 items located in oversize folder, call no. UBImul/B3",
            ["2 folders", "3 items located in oversize folder, call no. UBImul/B3"]
        )
        self.check_output_equality("5 eldritch horrors, no. 15-20", ["5 eldritch horrors, no. 15-20"])


if __name__ == "__main__":
    unittest.main()