import csv

from lxml import etree

from utilities.utilities import EADDir

def find_multiple_physdescs(ead):
    results = []
    parents = ead.tree.xpath("//physdesc")
    for parent in parents:
        tags = parent.xpath("extent")
        if len(tags) > 1:
            results.append([ead.filename, ead.tree.getpath(parent), len(tags), etree.tostring(etree.fromstring(etree.tostring(parent)))])

    return results

if __name__ == "__main__":
    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    e = EADDir(input_dir)
    results = e.characterize_dir(find_multiple_physdescs)

    with open("eads_with_multiple_extents.csv", mode="wb") as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerows(result)
