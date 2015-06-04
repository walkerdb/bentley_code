'''
Keywords to look out for:
	ips
	[n]x[n]
	rpm
	minute(s)
	[n]:[n]
	mm

'''

import re

import extent_constants


def split_extents(extent_text):

	# pre-split text cleanup
	extent_text = " ".join(extent_text.split())  # removes bad newlines and whitespace
	extent_text = extent_text.replace(" ft.", " feet")
	extent_text = extent_text.replace(" in.", " inches")
	extent_text = extent_text.replace(" inches reel", "-inch reel")
	extent_text = extent_text.replace("-in.", "-inch")
	extent_text = replace_written_numbers_with_digits(extent_text)

	# removal of elements containing split keywords that should not be split (to revert after splitting)
	regex_for_paren_text_with_and = r"(\(.*? and .*?\))"
	paren_text = re.findall(regex_for_paren_text_with_and, extent_text)
	if paren_text:
		paren_text = paren_text[0]
		extent_text = extent_text.replace(paren_text, "&&&")
	extent_text = extent_text.replace("lack and white", "&w")

	# split by keyword, then if any split element has no number,
	# re-append it to its previous neighbor using that same keyword
	extents = extent_text.split(" and ")
	extents = append_item_to_previous_if_no_numbers(extents, keyword=" and ")

	extents = filter(None, [item for extent in extents for item in extent.split(",")])
	extents = append_item_to_previous_if_no_numbers(extents, keyword=",")

	extents = filter(None, [item for extent in extents for item in extent.split(";")])
	extents = append_item_to_previous_if_no_numbers(extents, keyword=";")

	# reconstruction and final cleanup
	extents = [extent.replace("&w", "lack and white") for extent in extents]
	if paren_text:
		extents = [extent.replace("&&&", paren_text) for extent in extents]
	extents = [extent.strip() for extent in extents]

	return extents


def replace_written_numbers_with_digits(extent):
	written_numbers_dict = extent_constants.get_written_numbers_dict()
	extent = " {} ".format(extent)

	extent = extent.replace("(", "( ")
	extent = extent.replace("[", "[ ")

	for key, value in written_numbers_dict.items():
		if key in extent:
			extent = extent.replace(key, " " + value + " ")

	extent = extent.replace("(  ", "(")
	extent = extent.replace("( ", "(")
	extent = extent.replace("[ ", "[")

	return extent.strip(" ")


def append_item_to_previous_if_no_numbers(extents, keyword):
	for index, extent in enumerate(extents):
		if all([num not in extent for num in extent_constants.integers]) and index > 0:
			extents[index - 1] = extents[index - 1] + "{0}".format(keyword) + extents[index]
			extents.pop(index)
		elif " ips" in extents[index] and "reel" not in extents[index]:
			extents[index - 1] = extents[index - 1] + "{0}".format(keyword) + extents[index]
			extents.pop(index)
	return extents