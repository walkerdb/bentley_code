from collections import namedtuple
import re

from normalization.aspaceify_extents.aspaceify_extents.scripts.extent_constants import normalization_dict


def split_into_aspace_components(unparsed_extent, physdesc, portion, is_multiple=False):
    ASpaceExtent = namedtuple("ASpaceExtent", ["type_", "portion", "container_summary", "dimensions", "physfacet"])

    extent_data = extract_data_from_original_extent_text(unparsed_extent, portion)
    portion = create_portion(is_multiple, portion)

    return ASpaceExtent(type_=extent_data["extent_type"],
                        portion=portion,
                        container_summary=extent_data["container_summary"],
                        dimensions=extent_data["dimensions"],
                        physfacet=extent_data["physfacet"])


def extract_data_from_original_extent_text(unparsed_extent, physdesc):
    # this regex is literally the ugliest line of text I have ever seen.
    phys_dimensions_regex = r"\(?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?x[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?) ?(?:to|-|and)? ?(?:\d+?-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?x?[ -]?(?:\d+-?(?:\d+)?\/?(?:\d+)?\.?(?:\d+)?)? ?(?:inches|inch|cm\.?|in\.)?\)?"
    time_dimensions_regex = r"\d\d?\:\d\d\:?\d?\d?(?: min\.?| minutes)?|\(?ca\.? \d\d? min\.\)?"
    physfacet_regex = r'\(.*?\)| color and black[ -]and[ -]white| b&w| black[ -]and[ -]white|\bcolor\b| (?:\d \d/\d - )?\d \d/\d ips ?; \d(?:-\d\d)? inches| (?:\d[ -]\d/\d|\d\.\d\d) ips| \(dual track\)| ?\d\d?(?: ?\d?/\d)?(?:[ -]inch|")\.?(?= reel)|\d\d(?: \d/\d)? rpm'
    container_summary_regex = r"\b(?:located )in .*|\bin .*|\bformerly in .*"

    extent_text = unparsed_extent
    extent_text, phys_dimensions = extract_text_and_remove_from_extent_string(phys_dimensions_regex, extent_text)
    extent_text, time_dimensions = extract_text_and_remove_from_extent_string(time_dimensions_regex, extent_text)
    extent_text, physfacet = extract_text_and_remove_from_extent_string(physfacet_regex, extent_text)
    extent_text, container_summary = extract_text_and_remove_from_extent_string(container_summary_regex, extent_text)

    physfacet, container_summary = move_container_summaries_out_of_physfacet(physfacet, container_summary)
    container_summary = clean_container_summary(container_summary)

    extent_type_with_count = get_type_string(extent_text)
    extent_type_with_count, physfacet = normalize_type_to_controlled_value_and_update_physfacet(extent_type_with_count, physfacet)

    dimensions = join_with_semicolon(time_dimensions, phys_dimensions)

    if physdesc.xpath("physfacet"):
        join_with_semicolon(physfacet, physdesc.xpath("physfacet")[0].text)
    if physdesc.xpath("dimensions"):
        join_with_semicolon(physfacet, physdesc.xpath("dimensions")[0].text)
    if len(physdesc.xpath("extent")) > 1:
        # TODO - somehow get data for container summary extents. This might require changing how data is passed from the original extent grabber to exclude container summary extent tags
        pass

    return {"extent_text": extent_text,
            "phys_dimensions": phys_dimensions,
            "time_dimensions": time_dimensions,
            "dimensions": dimensions,
            "physfacet": physfacet,
            "container_summary": container_summary,
            "extent_type": extent_type_with_count}


def clean_container_summary(container_summary):
    if container_summary:
        if not container_summary.startswith("(") or not container_summary.endswith(")"):
            container_summary = "({0})".format(container_summary.strip("() "))

    return container_summary


def move_container_summaries_out_of_physfacet(physfacet, container_summary):
    if physfacet.startswith("in ") or physfacet.startswith("on "):
        container_summary = join_with_semicolon(text_to_add=physfacet, text_to_add_to=container_summary)
        physfacet = ""

    return physfacet, container_summary


def create_portion(is_multiple, portion):
    if not portion:
        portion = "part" if is_multiple else "whole"

    return portion


def extract_text_and_remove_from_extent_string(regex, extent_string):
    extracted_text = extract_regex_results_as_string(regex, extent_string)
    extent_string = re.sub(regex, "", extent_string) if extracted_text else extent_string
    return extent_string, extracted_text


def get_type_string(working_extent_string):
    type_ = working_extent_string
    type_ = " ".join(type_.split())
    type_ = type_.replace(" , ", " ")
    type_ = type_.replace(" ,; ", " ")
    type_ = type_.replace("()", "")
    type_ = type_.strip(" .;:,")
    return type_


def normalize_type_to_controlled_value_and_update_physfacet(type_string, physfacet_string):
    type_without_count = type_string.strip("1234567890 ")
    normalized_type, extra_physfacet = normalization_dict.get(type_without_count, ["", ""])

    if normalized_type:
        type_string = type_string.replace(type_without_count, normalized_type)

    if extra_physfacet:
        physfacet_string = join_with_semicolon(extra_physfacet, physfacet_string)

    return type_string, physfacet_string


def join_with_semicolon(text_to_add, text_to_add_to):
    new_text = text_to_add_to if text_to_add_to else ""
    if text_to_add_to:
        new_text += "; {0}".format(text_to_add)
    else:
        new_text += text_to_add

    return new_text.strip("; ")


def extract_regex_results_as_string(regular_expression, string_to_search):
    regex_return = re.findall(regular_expression, string_to_search)
    results_list = []
    results = ""
    if len(regex_return) > 0:
        for found_string in regex_return:
            results_list.append(found_string.strip("() "))
        results = " ".join("; ".join(results_list).split())

    return results
