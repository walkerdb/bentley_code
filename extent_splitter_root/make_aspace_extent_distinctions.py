from collections import namedtuple
import re


def split_into_component_parts(unparsed_extent):
	ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "number", "container_summary", "dimensions", "physfacet"])

	# this regex is literally the ugliest line of text I have ever seen.
	dimensions_regex = r"\(?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?x[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?(?:to|-)? ?(?:\d+?-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?x?[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?(?:inches|inch|cm\.?|in\.)?\)?"
	container_summary_regex = r" \(.*?\)| (?:located )in .*| in .*"
	physfacet_regex = r" color and black[ -]and[ -]white| b&w| black[ -]and[ -]white| color"

	audio_visual_keywords = ["tape", "cassette", "reel", " ips ", "vhs", "u-matic", " min."]

	type_ = unparsed_extent
	portion = ""
	number = ""
	container_summary = ""
	dimensions = ""
	physfacet = ""

	# find dimensions and remove them from the extent string
	dimensions = extract_regex_results_as_string(dimensions_regex, type_)
	type_ = re.sub(dimensions_regex, "", type_)

	# find physical facets and remove them from the extent string
	physfacet = extract_regex_results_as_string(physfacet_regex, type_)
	type_ = re.sub(physfacet_regex, "", type_)

	# find the container summary and remove from extent string
	container_summary = extract_regex_results_as_string(container_summary_regex, type_)
	type_ = re.sub(container_summary_regex, "", type_)

	# type is whatever remains. We need to clean up the mess a bit.
	type_ = " ".join(type_.split())
	type_ = type_.replace(" , ", " ")
	type_ = type_.replace(" ,; ", " ")
	type_ = type_.strip(" .;,")

	# if a container summary was found, enclose it in parens if it isn't already
	if container_summary:
		if not container_summary.startswith("("):
			container_summary = "({0})".format(container_summary.strip())

	output_extent = ASpaceExtent(type_=type_,
								 portion=portion,
								 number=number,
								 container_summary=container_summary,
								 dimensions=dimensions,
								 physfacet=physfacet)
	return output_extent


def extract_regex_results_as_string(regular_expression, string_to_search):
	regex_return = re.findall(regular_expression, string_to_search)
	results_list = []
	results = ""
	if len(regex_return) > 0:
		for dimension in regex_return:
			results_list.append(dimension)
		results = " ".join(results_list)
	results = results.strip()
	return results