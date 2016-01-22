import re

from lxml.builder import E

from ead_utilities.ead_utilities import EAD

def fix_romney(ead):
    extents = ead.tree.xpath("//extent")
    range_regex = r"(\d\d?)\-(\d\d?\d?)"
    for extent in extents:
        text = extent.text if extent.text else ""
        if not text.startswith("folder"):
            continue

        range = re.findall(range_regex, text)
        if len(range) == 0:
            continue

        start, end = range[0]
        total = int(end) - int(start) + 1
        extent.text = "{0} folders".format(total)
        physdesc = extent.getparent()
        did = physdesc.getparent()
        c0x = did.getparent()

        new_node = E("odd", E("p", text))

        c0x.insert(1, new_node)


if __name__ == "__main__":
    ead = EAD(filepath=r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all\romneyg.xml")
    fix_romney(ead)

    ead.prettyprint(output_dir="output")
