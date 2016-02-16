from os import listdir
from os import path

from lxml import etree


def get_all_extents(input_dir):
    eads = listdir(input_dir)
    eads = [ead for ead in eads if ead.endswith(".xml")]
    extents = []

    for ead in eads:
        root_tree = etree.parse(path.join(input_dir, ead))
        extents = root_tree.xpath("//extent")

        # only grab data for extent tags that don't represent containers
        extent_list = [[ead, root_tree.getpath(extent), extent.text.encode('utf-8') if extent.text else ""] for extent in extents if extent.get("altrender", "") != "carrier"]
        extents.append(extent_list)

    extents.reverse()

    return extents

if __name__ == "__main__":
    input_dir = r"S:\Curation\Student Work\Walker Boyle\source files\EADs\Master EAD 2015-06-12"
    get_all_extents(input_dir)
