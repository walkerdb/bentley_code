from __future__ import absolute_import
import csv

from main_projects.aspaceify_extents.scripts.extent_parser import split_into_extents
from tqdm import tqdm

CHARACTERIZE = False


def main():
    output = []
    longest_statement = 0
    filename = "../input/all_extents.csv"

    with open(filename, mode="r") as f:
        reader = csv.reader(f)
        reader.next()  # skip the header row

        for extent_row in tqdm(list(reader)):
            ead_filename, extent_xpath, extent_statement = extent_row
            extents_split = split_into_extents(extent_statement)

            for extent in extents_split:
                extent_row.append(extent)
            output.append(extent_row)

            if len(extents_split) > longest_statement:
                longest_statement = len(extents_split)

    with open("../extent_split.csv", mode="wb") as f:
        writer = csv.writer(f)

        header = ["EAD filename", "XPath to extent", "Original extent text"]
        for i in range(longest_statement):
            header.append("split extent segment {}".format(i + 1))
        writer.writerow(header)

        # If we are going to be doing any EAD modifications based on this list, we'll need to iterate over it in reverse
        # to keep the xpaths valid as we make multiple changes to the same file. It's easier to reverse it here than
        # in the transformation code
        output = reversed(output)

        for row in output:
            if len(row) < longest_statement:
                diff = longest_statement - len(row)
                row = add_blank_elements(row, diff)
            writer.writerow(row)


def add_blank_elements(row, number_of_elements_to_add):
    for i in range(number_of_elements_to_add):
        row.append("")
    return row


if __name__ == "__main__":
    main()