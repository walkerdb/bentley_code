from __future__ import absolute_import
import unittest
from collections import namedtuple

from normalization.aspaceify_extents.aspaceify_extents.scripts.make_aspace_extent_distinctions import split_into_aspace_components


class TestASpaceSplit(unittest.TestCase):
    def setUp(self):
        self.ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "container_summary", "dimensions", "physfacet"])

    def check_output_equality(self, extent, type_="", container_summary="", dimensions="", physfacet="", portion="whole", is_multiple=False):
        target_namedtuple = self.ASpaceExtent(type_=type_, portion=portion, physfacet=physfacet, container_summary=container_summary, dimensions=dimensions)
        generated_namedtuple = split_into_aspace_components(extent, portion, is_multiple)
        self.assertEqual(generated_namedtuple, target_namedtuple)

    def test_type_only(self):
        self.check_output_equality("5 volumes", type_="5 volumes")

    def test_paren_placed_in_container_summary(self):
        self.check_output_equality("5 linear feet (in 5 boxes)", type_="5 linear feet", container_summary="(in 5 boxes)")

    def test_in_section_placed_in_container_summary(self):
        self.check_output_equality("5 linear feet in 5 boxes", type_="5 linear feet", container_summary="(in 5 boxes)")

    def test_other_parens_placed_in_physfacet(self):
        self.check_output_equality("145 drawings (approximate)", type_="145 drawings", physfacet="approximate")

    def test_dimension_placed_in_dimensions(self):
        dimension_examples = [
            ("p, 2x4in.", "2x4in."),
            ("p, 2x4 in.", "2x4 in."),
            ("p, 2x4-5x8 cm.", "2x4-5x8 cm."),
            ("p, 20 x 40 cm", "20 x 40 cm"),
            ("p, 3-1/2x5 to 4x6-inch", "3-1/2x5 to 4x6-inch"),
            ("p, 79.5 x 113.8 cm. (31 x 44-3/8 inches)", "79.5 x 113.8 cm.; 31 x 44-3/8 inches")
        ]
        for dimension_example in dimension_examples:
            original_text, dimension = dimension_example
            self.check_output_equality(original_text, type_="p", dimensions=dimension)

    def test_complex_dimensions(self):
        self.check_output_equality("228 3-1/2x5 to 4x6-inch, prints in 5 boxes",
                                   type_="228 prints", dimensions="3-1/2x5 to 4x6-inch", container_summary="(in 5 boxes)")

    def test_black_and_white_put_in_phys_facet(self):
        self.check_output_equality("48 black and white 8x10-inch prints", type_="48 prints", dimensions="8x10-inch", physfacet="black and white")

    def test_horrific_extent_1(self):
        self.check_output_equality("26 3-1/4x4-1/4-inch, color and black-and-white; Polaroid prints",
                                   type_="26 photographs",
                                   dimensions="3-1/4x4-1/4-inch",
                                   physfacet="color and black-and-white",
                                   portion="whole")

    def test_horrific_extent_2(self):
        self.check_output_equality("236 3-1/2x5-1/2 and 4x6-inch, color prints",
                                   type_="236 prints",
                                   dimensions="3-1/2x5-1/2 and 4x6-inch",
                                   physfacet="color",
                                   portion="whole")

    def test_in_edge_case_1(self):
        self.check_output_equality("14 folders; formerly in binders", type_="14 folders", container_summary="(formerly in binders)")

    def test_in_edge_case_2(self):
        self.check_output_equality("(in 4 boxes)", type_="", container_summary="(in 4 boxes)")

    def test_reel_special_cases(self):
        self.check_output_equality("5 inch reel, 3 3/4 ips", type_="reels", physfacet="5 inch; 3 3/4 ips")
        self.check_output_equality('7" reel, 3.75 ips.', type_="reels", physfacet='7"; 3.75 ips')
        self.check_output_equality('1 10 1/2" reel', type_="1 reels", physfacet='10 1/2"')
        self.check_output_equality("3/4-inch reel", type_="reels", physfacet="3/4-inch")
        self.check_output_equality("1 sound tape reel: 7 1/2 ips; 5 inches", type_="1 audiotapes", physfacet="7 1/2 ips; 5 inches; reel-to-reel tapes")
        self.check_output_equality("2 sound tape reels: 3 3/4 ips; 7 inches", type_="2 audiotapes", physfacet="3 3/4 ips; 7 inches; reel-to-reel tapes")
        self.check_output_equality("5 sound tape reels (dual track): 7 1/2 ips; 7 inches", type_="5 audiotapes", physfacet="dual track; 7 1/2 ips; 7 inches; reel-to-reel tapes")
        self.check_output_equality('2 tapes, 3-3/4 ips', type_="2 tapes", physfacet="3-3/4 ips")
        self.check_output_equality("147 sound tape reels : 3 3/4 - 7 1/2 ips ; 5-10 inches", type_="147 audiotapes", physfacet="3 3/4 - 7 1/2 ips ; 5-10 inches; reel-to-reel tapes")

    def test_rpm(self):
        self.check_output_equality("33 1/3 rpm Phonograph Records", type_="phonograph records", physfacet="33 1/3 rpm")
        self.check_output_equality("set of 4 records, 45 rpm,33 1/3 rpm", type_="set of 4 records", physfacet="45 rpm; 33 1/3 rpm")

    def test_time_dimensions(self):
        self.check_output_equality("50:59", type_="", dimensions="50:59")
        self.check_output_equality("2:18 min.", type_="", dimensions="2:18 min.")
        self.check_output_equality("ca. 15 min.", type_="", dimensions="ca. 15 min.")
        self.check_output_equality("1 sound tape reel (13:08)", type_="1 audiotapes", dimensions="13:08", physfacet="reel-to-reel tapes")
        self.check_output_equality("1 sound tape reel (ca. 12 min.)", type_="1 audiotapes", dimensions="ca. 12 min.", physfacet="reel-to-reel tapes")
        self.check_output_equality("1 sound tape reel: ca. 3 min.", type_="1 audiotapes", dimensions="ca. 3 min.", physfacet="reel-to-reel tapes")

    def test_color_not_removed_when_part_of_other_words(self):
        self.check_output_equality("original drawings, pencil and colored pencil on tracing paper", type_="original drawings, pencil and colored pencil on tracing paper")

    def test_portion_assigns_part_correctly(self):
        self.check_output_equality("1 linear foot", type_="1 linear feet", portion="part", is_multiple=True)


if __name__ == "__main__":
    unittest.main()
