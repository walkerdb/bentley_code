from os import listdir
from os import path
import csv

from lxml import etree


def write_extents_to_csv(input_dir, output_dir="."):
    eads = listdir(input_dir)
    eads = [ead for ead in eads if ead.endswith(".xml")]

    with open(path.join(output_dir, "all_extents.csv"), mode="wb") as f:
        writer = csv.writer(f)
        for ead in eads:
            print(ead)
            root_tree = etree.parse(path.join(input_dir, ead))
            extents = root_tree.xpath("//extent")
            extent_list = [[ead, root_tree.getpath(extent), extent.text.encode('utf-8') if extent.text else ""] for extent in extents]
            writer.writerows(extent_list)

    with open(path.join(output_dir, "all_extents.csv"), mode="r") as f:
        reader = csv.reader(f)
        extent_list = reversed(list(reader))
        with open(path.join(output_dir, "all_extents_reversed.csv"), mode="wb") as g:
            writer = csv.writer(g)
            writer.writerows(extent_list)


if __name__ == "__main__":
    input_dir = r"S:\Curation\Student Work\Walker Boyle\source files\EADs\Master EAD 2015-06-12"
    write_extents_to_csv(input_dir)