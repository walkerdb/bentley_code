import re

def split_extents(extent_text):
	regex_to_split_by = r"\,|\[|\(| and | in " # splits by ",", "[", "(", " and ", and " in "
	extents = filter(None, re.split(regex_to_split_by, extent_text))
	extents = ["(" + extent if extent.endswith(")") else extent for extent in extents]
	extents = ["[" + extent if extent.endswith("]") else extent for extent in extents]
	extents = [extent.strip(" ") for extent in extents]

	return extents