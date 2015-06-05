from collections import namedtuple
import re


def split_into_component_parts(unparsed_extent):
	ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "number", "container_summary", "dimensions", "physfacet"])
	type_ = ""
	portion = ""
	number = ""
	container_summary = ""
	dimensions = ""
	physfacet = ""

	paren_regex = r" \(.*?\)"
	in_regex = r" in .*"

	container_summary = get_container_summary(container_summary, in_regex, paren_regex, unparsed_extent)


	type_ = unparsed_extent.split("(")[0].strip()
	type_ = type_.split(" in ")[0].strip()

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
			container_summary = "({0})".format(container_summary_list[0].strip())
	return container_summary
