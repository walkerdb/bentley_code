__author__ = 'wboyle'
import unittest
from collections import namedtuple

from make_aspace_extent_distinctions import split_into_component_parts


class TestASpaceSplit(unittest.TestCase):
	def setUp(self):
		self.ASpaceExtent = namedtuple("ASpaceExtent",
									   ["type_", "portion", "number", "container_summary", "dimensions", "physfacet"])

	def check_output_equality(self, extent, type_="", portion="", number="", container_summary="", dimensions="",
							  physfacet=""):
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
		self.fail("do this")


if __name__ == "__main__":
	unittest.main()