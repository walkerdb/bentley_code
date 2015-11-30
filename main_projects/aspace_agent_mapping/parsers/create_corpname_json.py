#
#
# name = name.replace("Dept.", "Department")
# "St."
# "no."
# "No."
# " Inc."
# "co."
#
# if name.endswith(")"):
#     qualifier = extract_qualifier
#
# names = name.split(". ", 2) # use a splitter that can tell if the period is a middle name abbreviation
# "B.E."
import re
import nltk.data

keys = [u"primary_name",
        u"subordinate_name_1",
        u"subordinate_name_2",
        u"qualifier",
        u"authority_id",
        u"source",
        u"sort_name_auto_generate",
        u"date_string",
        u"number",
        u"date_start",
        u"date_end"]


def parse_corpname(string, authority_id="", auth_source=""):
    string = string.strip(".")

    string, qualifier = extract_qualifier(string)

    primary_name, sub_name_1, sub_name_2 = split_into_component_entities(string)

    corpname_parsed = {u"primary_name":       unicode(primary_name),
                       u"subordinate_name_1": unicode(sub_name_1),
                       u"subordinate_name_2": unicode(sub_name_2),
                       u"qualifier":          unicode(qualifier.strip(" ()")),
                       u"authority_id":       unicode(authority_id),
                       u"source":             unicode(auth_source),
                       u"date_string":        unicode(""),
                       u"number":             unicode(""),
                       u"date_start":         unicode(""),
                       u"date_end":           unicode("")}

    return corpname_parsed


def extract_qualifier(string):
    qualifier_regex = re.compile(r"(\([^\(]*?\))$")
    qualifier = ""

    qualifier_match = re.findall(qualifier_regex, string)
    if qualifier_match:
        qualifier = qualifier_match[-1]

    string = string.replace(qualifier, "")

    return string, qualifier


def extract_names_from_split_components(parts):
    if len(parts) == 0:
        return "", "", ""
    if len(parts) == 1:
        return parts[0], "", ""
    if len(parts) == 2:
        return parts[0], parts[1], ""
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    else:
        return parts[0], parts[1], ". ".join(parts[2:]).replace("..", ".")


def split_into_component_entities(string):
    part_detector = nltk.data.load("tokenizers/punkt/english.pickle")
    string = re.sub("[Nn]o. ", "$$number$$", string)
    parts = part_detector.tokenize(string.strip())
    parts = [name.replace("$$number$$", "no. ") for name in parts]
    return [name.strip(". ") for name in extract_names_from_split_components(parts)]
