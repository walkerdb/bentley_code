import re

def split_extents(extent_text):
    # splits by " and ", " in ", and each of the following characters: ,([
    regex_to_split_by = re.compile(r"\,|\[|\(| and | in ")
    extent_list = filter(None, re.split(regex_to_split_by, extent_text))

    # the re.split() function removes the characters it splits by, so if we want to 
    # preserve the opening parentheses and brackets, we need to add those back
    extent_list = ["(" + extent if extent.endswith(")") else extent for extent in extent_list]
    extent_list = ["[" + extent if extent.endswith("]") else extent for extent in extent_list]

    # removing leading and trailing whitespace using the built-in strip() function
    extent_list = [extent.strip(" ") for extent in extent_list]

    return extent_list