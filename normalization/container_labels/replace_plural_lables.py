import os

from lxml import etree
from tqdm import tqdm


def replace_lables(input_directory):
    eads = [ead for ead in os.listdir(input_directory) if ead.endswith(".xml")]
    plurals = {"Boxes": "Box",
               "Bundles": "Bundle",
               "Display Panels": "Display Panel",
               "Drawers": "Drawer",
               "Folders": "Folder",
               "Oversize Boxes": "Oversize Box",
               "Oversize Folders": "Oversize Folder",
               "Oversize Frames": "Oversize Frame",
               "Oversize Volumes": "Oversize Volume",
               "Tubes": "Tube",
               "Volumes": "Volume"}

    for ead in tqdm(eads):
        tree = etree.parse(os.path.join(input_directory, ead))
        containers = tree.xpath("//container")
        modified = False

        for container in containers:
            label = container.attrib.get("label", "")
            if any(plural == label for plural in plurals.keys()):
                if "-" not in container.text:
                    container.attrib["label"] = plurals[label]
                    modified = True

        if modified:
            with open(os.path.join("output", ead), mode="w") as f:
                f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))


if __name__ == "__main__":
    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    replace_lables(input_dir)
