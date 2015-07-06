import csv
import re
import string

# Takes the extents.csv file and breaks up each long-form statement with multiple extents into its individual components
# Creates a historigram of each unique entry
# Counts total number of linear feet

def main():
    extents = []
    filename = "componentextents.csv"
    with open(filename, mode="r") as f:
        reader = csv.reader(f)
        for row in reader:
            extents.append(row[2])

    linearFeetCount(extents)
    splitAndCharacterizeExtents(extents)


def splitAndCharacterizeExtents(extents):
    # Splits extents by
    discrete_extents = splitExtentsIntoParts(extents)
    discrete_extents_with_extent_size = normalizeExtents(discrete_extents)

    discrete_extents_dict = buildHistorigramDict(discrete_extents_with_extent_size)
    writeSortedHistorigram(discrete_extents_dict, "component_extent_data.csv")


def splitExtentsIntoParts(extents):
    discrete_extents = []
    for extent in extents:
        extent = extent.split(",")
        for entry in extent:
            entry = entry.strip(" \t\n")
            if " and " in entry:
                entry = entry.split(" and ")
                for element in entry:
                    discrete_extents.append(element)
            elif entry.startswith("and "):
                entry = entry[4:]
            else:
                discrete_extents.append(entry)

    return discrete_extents


def normalizeExtents(discrete_extents):
    new_extents = []
    num_replace_regex = re.compile(r"(\d\d?\d?\d?) ")
    extent_size_regex = re.compile(r"^(\d\d?\d?\d?\.?\d?\d?) ")
    for extent in discrete_extents:
        extent_size = 0
        if all(letter not in extent for letter in string.ascii_letters):
            extent_name = extent.rstrip(".")
        elif "-inch" in extent[:10]:
            extent_name = extent[2:]
        else:
            try:
                extent_size = float(re.findall(extent_size_regex, extent.lstrip("ca. "))[0])
            except:
                print("failed to find extent size for" + ": " + extent)
            extent_name = extent.lstrip("0123456789 .+").rstrip(".")
            extent_name = re.sub(num_replace_regex, "[x] ", extent_name)
        new_extents.append([extent_name, extent_size])

    return new_extents

def buildHistorigramDict(list_of_items):
    historigram_dict = {}
    for item in list_of_items:
        item_name = item[0]
        item_size = item[1]
        if item_name not in historigram_dict:
            historigram_dict[item_name] = [1, item_size]
        else:
            historigram_dict[item_name][0] += 1
            historigram_dict[item_name][1] += item_size
    return historigram_dict

def writeSortedHistorigram(historigram_dict, filename):
    """
    Sorts a historigram dictionary by count and item name, then writes to a file
    :param historigram_dict: A dictionary whose key is a unique item (string), and
                             value is the count of times that item appears (int)
    :param filename: name of the file to write. Will overwrite any existing file with that name.
    """

    sorted_hist_data_as_list = sorted(sorted([(key, value[0], value[1]) for key, value in historigram_dict.items()],
                                             key=lambda x: x[0]), key=lambda x: -x[1])

    ## the above code, written out in long form
    #
    # item_list_with_counts = []
    # for item, item_instance_count in historigram_dict.items():
    #     item_list_with_counts.append([item, item_instance_count])
    #
    ## sort the list by count, and alphabetically for each count value
    # item_list_with_counts.sort()
    # item_list_with_counts.sort(key=lambda x: -x[1])

    with open(filename, mode="wb") as f:
        writer = csv.writer(f)
        header = ["extent name", "number of discrete appearances of extent type in EAD files", "total extent size through all collections"]
        writer.writerow(header)
        writer.writerows(sorted_hist_data_as_list)


def linearFeetCount(extents):
    expression = re.compile(r"(\d\d?\d?\.?\d?\d?) [lL]i?n.?(?:ear)? ?[Ff][oe]?[oe]?t")
    feet = 0.0
    for extent in extents:
        lf = re.findall(expression, extent)
        for item in lf:
            print(lf)
            feet += float(item)
    print(feet)


if __name__ == "__main__":
    main()