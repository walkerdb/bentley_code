import csv, re
from string import ascii_letters
from os import listdir
from lxml import etree

def split_sentence_into_parts(sentence):
    clauses = sentence.split(",")
    clauses = filter(None, [item for clause in clauses for item in clause.split(" and ")])
    clauses = filter(None, [item for clause in clauses for item in clause.split(" (")])
    clauses = ["(" + clause if clause.endswith(")") else clause for clause in clauses]

    discrete_items = []
    for clause in clauses:
        clause = clause.strip(" \t\n")
        if clause.startswith("and "):
            clause = clause[4:]

        discrete_items.append(clause)

    return discrete_items


def characterize_extents(discrete_extents):
    normalized_extents = []
    num_replace_regex = re.compile(r"(\d\d?\d?\d?) ")
    extent_size_regex = re.compile(r"^(\d\d?\d?\d?\.?\d?\d?) ")
    for extent in discrete_extents:
        extent_size = 0
        # check if extent name is entirely numerical
        if all(letter not in extent for letter in ascii_letters):
            extent_name = extent.rstrip(".")
        # account for edge-case
        elif "-inch" in extent[:10]:
            extent_name = extent[2:]
        # otherwise,
        else:
            try:
                extent_size = float(re.findall(extent_size_regex, extent.lstrip("ca. "))[0])
            except:
                print("failed to find extent size for" + ": " + extent)
            extent_name = extent.lstrip("0123456789 .+").rstrip(".")
            extent_name = re.sub(num_replace_regex, "[x] ", extent_name)
        normalized_extents.append([extent_name, extent_size])

    return normalized_extents

series = {}
def explore_series(source_directory=r"S:\Curation\Projects\Mellon\ArchivesSpace\ATeam_Migration\EADs\Real_Masters_all"):
    for filename in listdir(source_directory):
        if filename.endswith(".xml"):
            print(filename)
            tree = etree.parse(source_directory + "\\" + filename)
            inventory = tree.xpath("/ead/archdesc/dsc")[0]
            root_c01s = list(inventory)
            recurse_series(root_c01s)
    write_sorted_histogram(series, "series_exploration.csv")

def recurse_series(nodes):
    # some end condition, where full string is returned
    nodes = not isinstance(nodes, (list, tuple)) and [nodes] or nodes
    series_path = []

    def wrapped(node):
        # if len(series_path) == 1:
        #     temp = series_path.pop()
        #     temp = temp.strip(" \n\t")
        #     series_path.append(temp)
        series_string = "->".join([str(i) for i in series_path])

        series_path.append(node.get("level"))
        for child in list(node):
            if child.tag.startswith("c0"):
                wrapped(child)

        if all([not child.tag.startswith("c0") for child in list(node)]):
            key = "{0}->{1}".format(series_string, node.get("level"))
            key = key.lstrip("->")

            if key in series:
                series[key] += 1
            else:
                series[key] = 1
        series_path.pop()
        # print(series_string)

    for node in nodes:
        if node.tag.startswith("c0"):
            wrapped(node)

def build_histogram_dict(list_of_items):
    histogram_dict = {}
    for item in list_of_items:
        item_name = item
        if item_name not in histogram_dict:
            histogram_dict[item_name] = 1
        else:
            histogram_dict[item_name] += 1
    return histogram_dict


def write_sorted_histogram(histogram_dict, filename):
    """
    Sorts a histogram dictionary by count and item name, then writes to a file
    :param histogram_dict: A dictionary whose key is a unique item (string), and
                             value is the count of times that item appears (int)
    :param filename: name of the file to write. Will overwrite any existing file with that name.
    """

    sorted_hist_data_as_list = sorted(sorted([(key, value) for key, value in histogram_dict.items()],
                                             key=lambda x: x[0]), key=lambda x: -x[1])

    ## the above code, written out in long form
    #
    # item_list_with_counts = []
    # for item, item_instance_count in histogram_dict.items():
    #     item_list_with_counts.append([item, item_instance_count])
    #
    ## sort the list by count, and alphabetically for each count value
    # item_list_with_counts.sort()
    # item_list_with_counts.sort(key=lambda x: -x[1])

    with open(filename, mode="wb") as f:
        writer = csv.writer(f)
        header = ["series path", "number of instances"]
        writer.writerow(header)
        writer.writerows(sorted_hist_data_as_list)