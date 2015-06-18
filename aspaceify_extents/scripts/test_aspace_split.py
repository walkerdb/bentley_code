from __future__ import absolute_import
import unittest
from collections import namedtuple

from .make_aspace_extent_distinctions import split_into_aspace_components


class TestASpaceSplit(unittest.TestCase):
	def setUp(self):
		self.ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "container_summary", "dimensions", "physfacet"])

	def check_output_equality(self, extent, type_="", portion="", container_summary="", dimensions="", physfacet=""):
		target_namedtuple = self.ASpaceExtent(type_=type_, portion=portion, physfacet=physfacet, container_summary=container_summary, dimensions=dimensions)
		generated_namedtuple = split_into_aspace_components(extent)
		self.assertEqual(generated_namedtuple, target_namedtuple)

	def test_type_only(self):
		self.check_output_equality("5 volumes", type_="5 volumes", portion="part")

	def test_paren_placed_in_container_summary(self):
		self.check_output_equality("5 linear feet (in 5 boxes)", type_="5 linear feet", container_summary="(in 5 boxes)", portion="whole")

	def test_in_section_placed_in_container_summary(self):
		self.check_output_equality("5 linear feet in 5 boxes", type_="5 linear feet", container_summary="(in 5 boxes)", portion="whole")

	def test_dimension_placed_in_dimensions(self):
		dimension_examples = [
			("p, 2x4in.", "2x4in."),
			("p, 2x4 in.", "2x4 in."),
			("p, 2x4-5x8 cm.", "2x4-5x8 cm."),
			("p, 20 x 40 cm", "20 x 40 cm"),
			("p, 3-1/2x5 to 4x6-inch", "3-1/2x5 to 4x6-inch"),
			("p, 79.5 x 113.8 cm. (31 x 44-3/8 inches)", "79.5 x 113.8 cm. (31 x 44-3/8 inches)")
		]
		for dimension_example in dimension_examples:
			original_text, dimension = dimension_example
			self.check_output_equality(original_text, type_="p", dimensions=dimension, portion="part")

	def test_complex_dimensions(self):
		self.check_output_equality("228 3-1/2x5 to 4x6-inch, prints in 5 boxes",
								   type_="228 prints", dimensions="3-1/2x5 to 4x6-inch", container_summary="(in 5 boxes)", portion="part")

	def test_black_and_white_put_in_phys_facet(self):
		self.check_output_equality("48 black and white 8x10-inch prints", type_="48 prints", dimensions="8x10-inch", physfacet="black and white", portion="part")

	def test_horrific_extent_1(self):
		self.check_output_equality("26 3-1/4x4-1/4-inch, color and black-and-white; Polaroid prints",
								   type_="26 Polaroid prints",
								   dimensions="3-1/4x4-1/4-inch",
								   physfacet="color and black-and-white",
								   portion="part")

	def test_horrific_extent_2(self):
		self.check_output_equality("236 3-1/2x5-1/2 and 4x6-inch, color prints",
								   type_="236 prints",
								   dimensions="3-1/2x5-1/2 and 4x6-inch",
								   physfacet="color",
								   portion="part")

	def test_in_edge_case_1(self):
		self.check_output_equality("14 folders; formerly in binders", type_="14 folders", container_summary="(formerly in binders)", portion="part")

if __name__ == "__main__":
	unittest.main()