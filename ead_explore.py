import csv
import re
from os import listdir

from lxml import etree
from tqdm import tqdm

def characterize_series_in_directory(source_directory):
    series = {}
    for filename in tqdm(listdir(source_directory)):
        if filename.endswith(".xml"):
            tree = etree.parse(source_directory + "\\" + filename)
            attribute_paths = build_xml_tree_tag_paths(tree, filename=filename)
            for key, value in attribute_paths.items():
                series[key] = series.get(key, 0) + value
    write_sorted_histogram(series, "series_exploration.csv")


def build_xml_tree_tag_paths(etree_of_full_ead_dsc_node, tag="c0", attribute="level", filename=""):
    # Recursive function built to help characterize all possible c0x "level" hierarchies found in our EAD documents.
    # could be generalized to characterize the hierarchy of any regular attribute in any self-nesting tag by changing
    # the "tag" and "attribute" default values
    #
    # returns a dictionary containing each unique path, and a count of its instances. 
    # writes "problem" path locations to a csv.

    series = {}
    parent_etree_nodes = list(etree_of_full_ead_dsc_node.xpath("/ead/archdesc/dsc")[0])
    path_breadcrumb_list = []
    wonky_series_paths = ("item->file", "subseries->series",  "subseries->subseries", "collection", "fonds")

    with open("wonky_series_examples.csv", mode="ab") as f:
        writer = csv.writer(f)
        
        # recursion function
        def recurse_down_tree(node):
            if attribute:
                path_level_text = node.get(attribute)
            else:
                path_level_text = node.tag
            path_breadcrumb_string = "->".join([str(level) for level in path_breadcrumb_list])

            # add current level to series breadcrumb path
            path_breadcrumb_list.append(path_level_text)

            # for each child in the current node that starts with c0, recurse
            for child in list(node):
                if child.tag.startswith(tag):
                    recurse_down_tree(child)

            # if none of the current node's child tags start with c0, record the full path to node, and move on
            if all([not child.tag.startswith(tag) for child in list(node)]):
                key = "{0}->{1}".format(path_breadcrumb_string, path_level_text)
                key = key.lstrip("->") # bit of a hack-ish fix to remove leading arrows

                # add full series path to the recording dictionary if it isn't there already; else increment its count
                series[key] = series.get(key, 0) + 1
                
                if any(s in path_breadcrumb_string for s in wonky_series_paths):
                    xpath = etree_of_full_ead_dsc_node.getpath(node)
                    writer.writerow([filename, xpath, key])

            # if the code reaches this point, this is the end of this branch of the tree, so remove this leaf of the tree
            # from the path breadcrumb list
            path_breadcrumb_list.pop()

        for node in parent_etree_nodes:
            if node.tag.startswith("c0"):
                recurse_down_tree(node)

        return series


def build_histogram_dict(list_of_items, with_item_size=False):
    # given a list of items, builds a histogram of item frequency within that list
    # optionally can be given of list of item lists, in the format [item_name (a string), item_size (a number)], and will record cumulative
    # size along with pure instance counts.

    histogram_dict = {}
    for item in list_of_items:
        if with_item_size:
            item_name = item[0]
            item_size = float(item[1])
            if item_name not in histogram_dict:
                histogram_dict[item_name] = [1, item_size]
            else:
                histogram_dict[item_name][0] += 1
                histogram_dict[item_name][1] += item_size
        else:
            item_name = item
            histogram_dict[item_name] = histogram_dict.get(item_name, 0) + 1

    return histogram_dict


def write_sorted_histogram(histogram_dict, filename, with_item_size=False):
    """
    Sorts a histogram dictionary by EAD instance count and item name, then writes that date to a csv file

    :param histogram_dict: A dictionary whose key is a unique string, and whose value is either a numerical count value
                           or a list containing [instance_counts, cumulative_size]
    :param filename:       String containing the name of the file to write. Will overwrite any existing file with that name.
    :param with_item_size: Boolean describing whether the values of the passed histogram_dict also contain cumulative
                           item size counts
    """

    if with_item_size:
        sorted_hist_data_as_list = sorted(sorted([(key, value[0], value[1]) for key, value in histogram_dict.items()],
                                                 key=lambda x: x[0]), key=lambda x: -x[1][0])
    else:
        sorted_hist_data_as_list = sorted(sorted([(key, value) for key, value in histogram_dict.items()],
                                                 key=lambda x: x[0]), key=lambda x: -x[1])

    with open(filename, mode="wb") as f:
        writer = csv.writer(f)
        if with_item_size:
            header = ["name", "number of appearances within EADs", "cumulative size"]
        else:
            header = ["name", "number of appearances within EADs"]
        writer.writerow(header)
        writer.writerows(sorted_hist_data_as_list)

def get_list_of_xml_files_in_directory(directory):

    files = []
    for filename in listdir(directory):
        if filename.endswith(".xml"):
            files.append(filename)
    return files


if __name__ == "__main__":
    characterize_series_in_directory(r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all")
