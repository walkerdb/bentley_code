__author__ = 'wboyle'
import unittest
from collections import namedtuple

from make_aspace_extent_distinctions import split_into_component_parts


class TestASpaceSplit(unittest.TestCase):
	def setUp(self):
		self.ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "number", "container_summary", "dimensions", "physfacet"])

	def check_output_equality(self, extent, type_="", portion="", number="", container_summary="", dimensions="", physfacet=""):
		target_tuple = self.ASpaceExtent(type_=type_,
										 portion=portion,
										 number=number,
										 container_summary=container_summary,
										 dimensions=dimensions,
										 physfacet=physfacet)
		extent_tuple = split_into_component_parts(extent)
		self.assertEqual(extent_tuple, target_tuple)


	def test_paren_placed_in_container_summary(self):
		self.check_output_equality("5 linear feet (in 5 boxes)", type_="5 linear feet",
								   container_summary="(in 5 boxes)")

	def test_in_section_placed_in_container_summary(self):
		self.check_output_equality("5 linear feet in 5 boxes", type_="5 linear feet", container_summary="(in 5 boxes)")

	def test_dimension_placed_in_dimensions(self):
		dimension_examples = [
			("p, 2x4in.", "2x4in."),
			("p, 2x4 in.", "2x4 in."),
			("p, 2x4-5x8 cm.", "2x4-5x8 cm."),
			("p, 20 x 40 cm", "20 x 40 cm"),
			("p, 3-1/2x5 to 4x6-inch", "3-1/2x5 to 4x6-inch"),
			("p, 79.5 x 113.8 cm. (31 x 44-3/8 inches)", "79.5 x 113.8 cm. (31 x 44-3/8 inches)")
		]
		for dimension in dimension_examples:
			original, dim = dimension
			self.check_output_equality(original, type_="p", dimensions=dim)


	def test_complex_dimensions(self):
		self.check_output_equality("228 3-1/2x5 to 4x6-inch, color prints in 5 boxes",
								   type_="228 color prints", dimensions="3-1/2x5 to 4x6-inch", container_summary="(in 5 boxes)")


if __name__ == "__main__":
	unittest.main()