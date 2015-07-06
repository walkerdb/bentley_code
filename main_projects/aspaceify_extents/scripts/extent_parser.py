from __future__ import absolute_import
import re
from string import ascii_letters

from aspaceify_extents.scripts import extent_constants


def split_into_extents(extent_text):

    extent_text = cleanup_text(extent_text)
    extent_text, paren_text = remove_edge_case_elements(extent_text)

    # split by keyword, then if any split element has no number,
    # re-append it to its previous neighbor using that same keyword
    extents = extent_text.split(",")
    extents = reappend_non_extent_items(extents, keyword=",")

    extents = list(filter(None, [item for extent in extents for item in extent.split(" and ")]))
    extents = reappend_non_extent_items(extents, keyword=" and ")

    extents = list(filter(None, [item for extent in extents for item in extent.split(";")]))
    extents = reappend_non_extent_items(extents, keyword=";")

    # reconstruction and final cleanup
    extents = replace_edge_case_elements(extents, paren_text)
    extents = [extent.strip() for extent in extents]
    extents = [extent.rstrip(")") if (extent.endswith(")") and "(" not in extent) else extent for extent in extents]

    return extents


def cleanup_text(extent_text):
    extent_text = " ".join(extent_text.split())  # removes bad newlines and whitespace
    extent_text = extent_text.replace(" black-and-white", " black and white")
    extent_text = extent_text.replace(" black & white", " black and white")
    extent_text = extent_text.replace("ca. ", "")
    extent_text = extent_text.replace(" col.", " color")
    extent_text = extent_text.replace(" ft.", " feet")
    extent_text = extent_text.replace("-in.", "-inch")
    extent_text = extent_text.replace(" in.", " inches")
    extent_text = extent_text.replace(" inches reel", "-inch reel")  # revert above change for reel case
    extent_text = extent_text.replace(" outsize", " oversize")
    extent_text = replace_written_numbers_with_digits(extent_text)
    return extent_text


def remove_edge_case_elements(extent_text):
    regex_for_paren_text = r"(\(.*?\))"
    paren_text = re.findall(regex_for_paren_text, extent_text)
    if paren_text:
        for text in paren_text:
            if " and " in text:
                extent_text = extent_text.replace(text, "&&&")
                paren_text = text
                break

        if isinstance(paren_text, list):
            paren_text = ""
    extent_text = extent_text.replace("lack and white", "&w")
    return extent_text, paren_text


def replace_edge_case_elements(extents, paren_text):
    extents = [extent.replace("&w", "lack and white") for extent in extents]
    if paren_text:
        extents = [extent.replace("&&&", paren_text) for extent in extents]
    return extents


def replace_written_numbers_with_digits(extent):
    written_numbers_dict = extent_constants.numbers_dict
    extent = " {} ".format(extent)

    extent = extent.replace("(", "( ")
    extent = extent.replace("[", "[ ")

    for key, value in written_numbers_dict.items():
        if key in extent:
            extent = extent.replace(key, " {0} ".format(value))

    extent = extent.replace("(  ", "(")
    extent = extent.replace("( ", "(")
    extent = extent.replace("[ ", "[")

    return extent.strip()


def reappend_non_extent_items(extents, keyword):
    dimensions_regex = r"\d\d?\d?\.?-? ?\d?/?\d?\d? ?x ?\d\d?\d?\.?-? ?\d?/?\d?\d?"

    for index, extent in enumerate(extents):
        if index > 0:
            # primary function - if extent has no numbers, re-append to its previous neighbor
            if extent.isalpha():
                extents[index - 1] = extents[index - 1] + "{0}".format(keyword) + extents[index]
                extents.pop(index)

            ### edge cases ###
            # reconstruct comma-formatted numbers
            elif all([keyword is ",", extent[:3].isdigit(), extents[index - 1][-1].isdigit()]):
                extents[index - 1] = extents[index - 1] + "{0}".format(",") + extents[index]
                extents.pop(index)

            # re-append dimensions-only extents to previous neighbor
            elif all(char not in extent_constants.integers for char in re.sub(dimensions_regex, "", extent)):
                extents[index - 1] = extents[index - 1] + "{0}".format(keyword) + extent
                extents.pop(index)

            # audio formatting
            elif " ips" in extent and "reel" not in extent:
                extents[index - 1] = extents[index - 1] + "{0}".format(keyword) + extent
                extents.pop(index)

            elif re.search(r"^\d\d? inches$", extent) is not None:
                extents[index - 1] = extents[index - 1] + "{0}".format(keyword) + extent
                extents.pop(index)

            elif "inches" in extent and all([char not in extent.replace("inches", "") for char in ascii_letters]):
                extents[index - 1] = extents[index - 1] + "{0}".format(keyword) + extent
                extents.pop(index)

            elif "rpm" in extent and all([char not in extent.replace("rpm", "") for char in ascii_letters]):
                extents[index - 1] = extents[index - 1] + "{0}".format(",") + extent
                extents.pop(index)

            # number ranges and call numbers should be re-appended
            elif extent.startswith(" no.") or extent.startswith(" call no."):
                extents[index - 1] = extents[index - 1] + "{0}".format(",") + extent
                extents.pop(index)

            # specific one-time fixes
            elif extent in "60 second PSA":
                extents[index - 1] = extents[index - 1] + "{0}".format(" and ") + extents[index]
                extents.pop(index)

            elif extent in "1913":
                extents[index - 1] = extents[index - 1] + "{0}".format(" and ") + extents[index]
                extents.pop(index)

            elif extents[-1] in "1 disc (sides 1":
                extents[index - 1] = extents[index - 1] + "{0}".format(" and ") + extents[index]
                extents.pop(index)

    return extents