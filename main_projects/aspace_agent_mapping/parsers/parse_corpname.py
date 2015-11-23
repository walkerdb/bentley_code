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
# names = name.split(". ") # use a splitter that can tell if the period is a middle name abbreviation
# "B.E."
import re

keys = [u"primary_name",
        u"subordinate_name_1",
        u"subordinate_name_2",
        u"qualifier",
        u"authority_id",
        u"source",
        u"sort_name_auto_generate",
        u"date_string",
        u"auth",
        u"number",
        u"date_start",
        u"date_end"]


def parse_corpname(string):
    string = string.strip(".")

    string, qualifier = extract_qualifier(string)

    if string.endswith(")"):


    corpname_parsed = {u"primary_name":       unicode(primary_name),
                       u"subordinate_name_1": unicode(""),
                       u"subordinate_name_2": unicode(""),
                       u"qualifier":          unicode(""),
                       u"authority_id":       unicode(""),
                       u"source":             unicode(""),
                       u"date_string":        unicode(""),
                       u"auth":               unicode(""),
                       u"number":             unicode(""),
                       u"date_start":         unicode(""),
                       u"date_end":           unicode("")}

    return corpname_parsed


def extract_qualifier(string):
    qualifier_regex = re.compile(r"(\([^\(]*?\))^")
    qualifier = ""

    qualifier_match = re.findall(qualifier_regex, string)
    if qualifier_match:
        qualifier = qualifier_match[-1]
    pass
