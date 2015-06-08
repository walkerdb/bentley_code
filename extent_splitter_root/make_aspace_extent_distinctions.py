from collections import namedtuple
import re


def split_into_component_parts(unparsed_extent):
	ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "number", "container_summary", "dimensions", "physfacet"])

	# this regex is literally the ugliest line of text I have ever seen.
	dimensions_regex = r"\(?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?x[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?(?:to|-)? ?(?:\d+?-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?x?[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?(?:inches|inch|cm\.?|in\.)?\)?"
	paren_regex = r" \(.*?\)"
	in_regex = r" in .*"

	type_ = unparsed_extent
	portion = ""
	number = ""
	container_summary = ""
	dimensions = ""
	physfacet = ""

	# find any dimensions and extract them
	regex_return = re.findall(dimensions_regex, unparsed_extent)
	dimension_list = []
	if len(regex_return) > 0:
		for dimension in regex_return:
			dimension_list.append(dimension)
		dimensions = " ".join(dimension_list)
	type_ = re.sub(dimensions_regex, "", type_)

	# find the container summary if there is one
	container_summary = get_container_summary(container_summary, in_regex, paren_regex, type_)

	# construct type by removing everything else, then cleaning up the remnants
	type_ = type_.replace(container_summary, "")
	type_ = type_.replace(" , ", " ")
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


def get_container_summary(container_summary, in_regex, paren_regex, unparsed_extent):
	container_summary_list = re.findall(paren_regex, unparsed_extent)
	if container_summary_list:
		if len(container_summary_list) == 1:
			container_summary = container_summary_list[0].strip()
		elif len(container_summary_list) > 1:
			print("too many container summaries, ahhhhhhh")
			for container in container_summary_list:
				container_summary += "{0}; ".format(container.strip())
			container_summary.rstrip("; ")
		else:
			container_summary = ""
	if not container_summary:
		container_summary_list = re.findall(in_regex, unparsed_extent)
		if container_summary_list:
			container_summary = container_summary_list[0]
	return container_summary
