import os
import csv
from pprint import pprint
from collections import defaultdict

from lxml import etree
from tqdm import tqdm


# change to your input directory
input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'


def characterize_single_tag_attribute(ead_input_dir, tag_name, attribute_name):
    '''
    Reads all eads in the input directory to create counts of each unique attribute value
    found for the given attribute in the given tag type

    Use "c0x" as the tag type if you want the attributes of every type of c0-level tag.
    '''

    # create list of valid files to run through
    files = [ead for ead in os.listdir(ead_input_dir) if ead.endswith(".xml")]

    # init values dictionary
    values = {}

    # iterate through all valid eads
    for ead in tqdm(files):
        tree = etree.parse(os.path.join(ead_input_dir, ead))

        ## extract all relevant tags from the tree
        # special case for the "c0x" tag value
        if tag_name == "c0x":
            elements_list = [tree.xpath("//c0{}".format(i)) for i in range(1, 10)]
            elements = []
            for element in elements_list:
                elements += list(element)

        # normal case
        else:
            elements = tree.xpath("//{}".format(tag_name))

        # add attribute value to the values dictionary, and increment its count
        for element in elements:
            value = element.attrib.get(attribute_name, "")
            values[value] = values.get(value, 0) + 1

    # write results to file (filename based off of tag and attribute names)
    with open("{0}_{1}_counts.csv".format(tag_name, attribute_name), mode="wb") as f:
        writer = csv.writer(f)
        header = ["attribute value", "count"]
        value_rows = sorted([[attribute, count] for attribute, count in values.items()])

        writer.writerow(header)
        writer.writerows(value_rows)

    pprint(values)


def characterize_all_attributes(ead_input_dir):
    files = [ead for ead in os.listdir(ead_input_dir) if ead.endswith(".xml")]
    attributes = defaultdict(lambda: defaultdict(dict))
    tag_totals = {}
    tag_attribute_totals = {}
    forbidden_attribs = ["normal", "authfilenumber", "publicid", "href", "id", "encodinganalog"]

    # iterate through all valid eads
    for ead in tqdm(files):
        tree = etree.parse(os.path.join(ead_input_dir, ead))

        # iterate through all elements in the tree
        for element in tree.iter():
            tag = element.tag

            # don't know why, but some elements don't have tag attributes. Maybe they're comments or something
            try:
                # merge all c0x tags for comparison purposes
                tag = "c0x" if tag.startswith("c0") or tag.startswith("c1") else tag

                # increment the total count for this tag type
                tag_totals[tag] = tag_totals.get(tag, 0) + 1

            except AttributeError:
                continue

            # if there are any attributes in this element, start characterizing
            if len(element.attrib) > 0:

                # iterate through each attribute/value pair in the element's attribute list
                for attribute, value in element.attrib.items():

                    # increment the count for this tag/attribute combination
                    temp_key = "{0}_{1}".format(tag, attribute)
                    tag_attribute_totals[temp_key] = tag_attribute_totals.get(temp_key, 0) + 1

                    # if the attribute does not appear in the forbidden attribute list, increment its tag/attrib/value count
                    if all(attribute != attrib for attrib in forbidden_attribs):
                        attributes[tag][attribute][value] = attributes[tag][attribute].get(value, 0) + 1

    # write results to file (filename based off of tag and attribute names)
    with open("all_counts.csv".format(tag_name, attribute_name), mode="wb") as f:
        writer = csv.writer(f)
        header = ["tag", "attribute", "attribute value", "count", "percentage of all tags"]
        output_rows = []
        for tag, attribute_dict in attributes.items():
            for attribute, value_dict in attribute_dict.items():
                for value, count in value_dict.items():
                    tag_percentage = float(count) / float(tag_totals[tag])
                    output_rows.append([tag, attribute, value, count, "{0:.2f}".format(tag_percentage * 100)])

                total_tags_with_attribute = tag_attribute_totals["{0}_{1}".format(tag, attribute)]
                if tag_totals[tag] != total_tags_with_attribute:
                    difference = tag_totals[tag] - total_tags_with_attribute
                    difference_percentage = float(difference) / float(tag_totals[tag])
                    output_rows.append([tag, attribute, "[tags without this attribute]", difference, "{0:.2f}".format(difference_percentage * 100)])

        output_rows = sorted(sorted(sorted(output_rows, key=lambda x: -x[3]), key=lambda x: x[1]), key=lambda x: x[0])
        writer.writerow(header)
        writer.writerows(output_rows)

    pprint(output_rows)


if __name__ == "__main__":
    # change to the tag/attribute combo you're looking to characterize
    # tag_name = "container"
    # attribute_name = "type"

    # characterize_single_tag_attribute(input_dir, tag_name=tag_name, attribute_name=attribute_name)

    characterize_all_attributes(input_dir)