from lxml.builder import E

from utilities.utilities import EAD

def fix_romney(ead):
    extents = ead.tree.xpath("//extent")

    for extent in extents:
        text = extent.text if extent.text else ""
        if any([text.startswith(i) for i in "0123456789"]):
            continue
        physdesc = extent.getparent()

        physdesc.remove(extent)
        new_node = E("physfacet", text)
        physdesc.append(new_node)


if __name__ == "__main__":
    ead = EAD(filepath=r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all\athdept.xml")
    fix_romney(ead)

    ead.prettyprint(output_dir="output")