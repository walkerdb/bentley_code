from os import listdir
from os import path

from lxml import etree
from tqdm import tqdm


def get_all_extents(input_dir):
    eads = listdir(input_dir)
    eads = [ead for ead in eads if ead.endswith(".xml")]
    extent_list = []

    for ead in tqdm(eads, desc="extracting original extents..."):
        root_tree = etree.parse(path.join(input_dir, ead))
        extents = root_tree.xpath("//extent")

        # only grab data for extent tags that don't represent containers
        for extent in extents:
            if extent.get("altrender", ""):
                continue
            extent_list.append([ead, root_tree.getpath(extent), extent.text.encode("utf-8") if extent.text else ""])

    extent_list.reverse()

    return extent_list

if __name__ == "__main__":
    input_dir = r"S:\Curation\Student Work\Walker Boyle\source files\EADs\Master EAD 2015-06-12"
    get_all_extents(input_dir)
