from collections import namedtuple
import re


def split_into_aspace_components(unparsed_extent):
	ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "container_summary", "dimensions", "physfacet"])

	# this regex is literally the ugliest line of text I have ever seen.
	phys_dimensions_regex = r"\(?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?x[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?(?:to|-|and)? ?(?:\d+?-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?x?[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?(?:inches|inch|cm\.?|in\.)?\)?"
	time_dimensions_regex = r"\d\d?\:\d\d\:?\d?\d?(?: min\.?| minutes)?|\(?ca\.? \d\d? min\.\)?"
	physfacet_regex = r' color and black[ -]and[ -]white| b&w| black[ -]and[ -]white|\bcolor\b| (?:\d \d/\d - )?\d \d/\d ips ?; \d(?:-\d\d)? inches| (?:\d[ -]\d/\d|\d\.\d\d) ips| \(dual track\)| ?\d\d?(?: ?\d?/\d)?(?:[ -]inch|")\.?(?= reel)|\d\d(?: \d/\d)? rpm'
	container_summary_regex = r"\(.*?\)|\b(?:located )in .*|\bin .*|\bformerly in .*"

	working_extent_string = unparsed_extent

	# find physical dimensions and remove them from the extent string
	phys_dimensions = extract_regex_results_as_string(phys_dimensions_regex, working_extent_string)
	working_extent_string = re.sub(phys_dimensions_regex, "", working_extent_string) if phys_dimensions else working_extent_string

	# find time dimensions and remove them from the extent string
	time_dimensions = extract_regex_results_as_string(time_dimensions_regex, working_extent_string)
	working_extent_string = re.sub(time_dimensions_regex, "", working_extent_string) if time_dimensions else working_extent_string

	# find physical facets and remove them from the extent string
	physfacet = extract_regex_results_as_string(physfacet_regex, working_extent_string)
	working_extent_string = re.sub(physfacet_regex, "", working_extent_string) if physfacet else working_extent_string

	# find the container summary and remove from extent string
	container_summary = extract_regex_results_as_string(container_summary_regex, working_extent_string)
	working_extent_string = re.sub(container_summary_regex, "", working_extent_string) if container_summary else working_extent_string

	# type is whatever remains. We need to clean up the mess a bit.
	type_ = working_extent_string
	type_ = " ".join(type_.split())
	type_ = type_.replace(" , ", " ")
	type_ = type_.replace(" ,; ", " ")
	type_ = type_.replace("()", "")
	type_ = type_.strip(" .;:,")

	# setting portion tag
	portion = "part"
	if "linear" in type_:
		portion = "whole"

	# make sure the container summary is enclosed in parens
	if container_summary:
		if not container_summary.startswith("(") or not container_summary.endswith(")"):
			container_summary = "({0})".format(container_summary.strip("() "))

	# construct final dimensions from time and physical dimensions
	dimensions = time_dimensions + phys_dimensions

	output_extent = ASpaceExtent(type_=type_,
								 portion=portion,
								 container_summary=container_summary,
								 dimensions=dimensions,
								 physfacet=physfacet)
	return output_extent


def extract_regex_results_as_string(regular_expression, string_to_search):
	regex_return = re.findall(regular_expression, string_to_search)
	results_list = []
	results = ""
	if len(regex_return) > 0:
		for found_string in regex_return:
			results_list.append(found_string.strip("() "))
		results = " ".join("; ".join(results_list).split())

	return results