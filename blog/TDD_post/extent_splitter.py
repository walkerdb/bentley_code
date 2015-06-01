import re

integers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

ones_dict = {
	" one ": "1",
	" two ": "2",
	" three ": "3",
	" four ": "4",
	" five ": "5",
	" six ": "6",
	" seven ": "7",
	" eight ": "8",
	" nine ": "9"
}
ten_to_nineteen_dict = {
	" ten ": "10",
	" eleven ": "11",
	" twelve ": "12",
	" thirteen ": "13",
	" fourteen ": "14",
	" fifteen ": "15",
	" sixteen ": "16",
	" seventeen ": "17",
	" eighteen ": "18",
	" nineteen ": "19",
}

tens_dict = {
	"twenty-": "2",
	"thirty-": "3",
	"forty-": "4",
	"fifty-": "5",
	"sixty-": "6",
	"seventy-": "7",
	"eighty-": "8",
	"ninety-": "9"
}

full_numbers_dict = {}

for tens_key, tens_value in tens_dict.items():
	for ones_key, ones_value in ones_dict.items():
		full_numbers_dict[" " + tens_key + ones_key.lstrip(" ")] = tens_value + ones_value

full_numbers_dict.update(ten_to_nineteen_dict)
full_numbers_dict.update(ones_dict)


def split_extents(extent_text):
	if "lack and white" in extent_text:
		extent_text = extent_text.replace("lack and white", "&w")

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
	extent_list = reconstruct_extent_if_no_numbers(extent_list)

	return extent_list


def reconstruct_extent_if_no_numbers(extent_list):
	for index, extent in enumerate(extent_list):
		if len(extent_list) > 1 and all([num not in extent for num in integers]):
			if index > 0:
				if extent.startswith("(") or extent.startswith("["):
					extent_list[index - 1] = extent_list[index - 1] + " " + extent_list[index]
				else:
					extent_list[index - 1] = extent_list[index - 1] + ", " + extent_list[index]
				extent_list.pop(index)
	return extent_list