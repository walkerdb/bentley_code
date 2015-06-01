import re
import extent_constants


def split_extents(extent_text):
	manual_text_to_add = []
	if "lack and white" in extent_text:
		extent_text = extent_text.replace("lack and white", "&w")
	if "\n" in extent_text:
		extent_text = " ".join(extent_text.split("\n"))
	if "  " in extent_text:
		extent_text = " ".join(extent_text.split())

	# splits by " and ", " in ", and each of the following characters: ,([
	regex_to_split_by = r",|\[|\(| and | in |;"
	extent_list = filter(None, re.split(regex_to_split_by, extent_text))

	# the re.split() function removes the characters it splits by, so if we want to
	# preserve the opening parentheses and brackets, we need to add those back
	extent_list = ["(" + extent if extent.endswith(")") else extent for extent in extent_list]
	extent_list = ["[" + extent if extent.endswith("]") else extent for extent in extent_list]

	# removing leading and trailing whitespace using the built-in strip() function
	extent_list = [extent.strip(" ") for extent in extent_list]
	extent_list = [extent.replace("&w", "lack and white") for extent in extent_list]
	extent_list = replace_written_numbers_with_digits(extent_list)
	extent_list = reconstruct_extent_if_no_numbers(extent_list)

	return extent_list


def reconstruct_extent_if_no_numbers(extent_list):
	for index, extent in enumerate(extent_list):
		if len(extent_list) > 1 and all([num not in extent for num in extent_constants.integers]):
			if index > 0:
				if extent.startswith("(") or extent.startswith("["):
					extent_list[index - 1] = extent_list[index - 1] + " " + extent_list[index]
				else:
					extent_list[index - 1] = extent_list[index - 1] + ", " + extent_list[index]
				extent_list.pop(index)
	return extent_list


def replace_written_numbers_with_digits(extent_list):
	written_numbers_dict = extent_constants.get_written_numbers_dict()
	extents_with_integer_numbers = []

	for extent in extent_list:
		extent = " {} ".format(extent)
		extent = extent.replace("(", "( ")
		extent = extent.replace("[", "[ ")

		for key, value in written_numbers_dict.items():
			if key in extent:
				extent = extent.replace(key, " " + value + " ")

		extent = extent.replace("( ", "(")
		extent = extent.replace("[ ", "[")

		extents_with_integer_numbers.append(extent.strip(" "))

	return extents_with_integer_numbers