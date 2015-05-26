'''
Meant to explore and characterize the myriad ways EADs end up with empty <unittitle> tags

Reads the emptytitle.csv made by Dallas' getemptytitles.py and outputs two files:
    1. A text file containing the filename, xpath, and tag content of each problem node from emptytitles.csv
    2. A CSV containing an entry for each unique tag structure found while processing the first step, with counts for
       number of found instances for each type.

'''


import csv
from lxml import etree

origin = 'S:/Curation/Student Work/Walker Boyle/Test environment/source files/EADs/Master EAD 2015-05-04/'
parser = etree.XMLParser(remove_blank_text=True) # this makes pretty_print work properly when using tostring function.
                                                 # Has to be passed as the second argument to etree.parse when first
                                                 # reading the data.
counts = {}


def main():
    problem_node_data = []

    # read the empty title input CSV, grab the nodes in question from each EAD, and append that info to a list
    with open("emptytitles.csv", mode="r") as f:
        reader = csv.reader(f)
        for row in reader:
            retrieved_data = read_data(row)
            problem_node_data.append(retrieved_data)

    # write the contents of the node list to a file for perusal
    write_nodes_and_locations(problem_node_data)

    # I also want to get a count of how many unique kinds of unittitle errors there are, and how many examples of each
    # appear in the EADs.
    write_node_type_counts()


def read_data(row):
    filename = row[0]
    xpath = row[1]

    path = origin + filename
    with open(path, mode="r") as f:
        tree = etree.parse(f, parser)

    problem_node = tree.xpath(xpath)[0]

    # add a record of this kind of broken node (this particular arrangement of tags) to the count dictionary
    node_copy = etree.XML(etree.tostring(problem_node))
    add_abstracted_node_to_dict(node_copy)

    tag = etree.tostring(problem_node, pretty_print=True)
    data = [filename, xpath, tag]
    return data


def add_abstracted_node_to_dict(problem_node):
    # characterizes the kind of node this is by tag and text content
    for element in problem_node.iter():
        tag = element.tag
        if tag.startswith("c0"):
            element.tag = "c0x"
        if element.text:
            element.text = element.text.strip(" \n\t") # some tags only contain whitespace - those shouldn't count
            if element.text:
                element.text = "text"
        attributes = element.attrib
        for attribute in attributes:
            attributes[attribute] = "text"

    # normalize empty tags (self-closing vs. pair), create dictionary key based on pretty-printed version of abstracted node
    normalized_string = etree.tostring(problem_node, method="html")
    node_type_key = etree.tostring(etree.XML(normalized_string, parser), pretty_print=True)

    # adding a count to the counts dictionary for this key
    if node_type_key not in counts:
        counts[node_type_key] = 1
    else:
        counts[node_type_key] += 1


def write_nodes_and_locations(tag_list):
    with open("output/all_empty_tags.xml", mode="w") as f:
        for row in tag_list:
            f.write("{0}: {1}".format(row[0], row[1]) + "\n")
            f.write(row[2] + "\n")


def write_node_type_counts():
    # create a list of tuples based on the counts dictionary, sorted by count, then write to file
    data = sorted([(key, value) for key, value in counts.items()], key=lambda x: -x[1])

    with open("output/empty_title_tag_types_with_counts", mode="w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == "__main__":
    main()
