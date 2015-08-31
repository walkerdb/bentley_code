import csv

from utilities.utilities import EADDir

def find_nested_tags(ead):
    results = []
    for node in ead.tree.iter():
        tag = node.tag
        if len(list(node)) != 1:
            continue
        if list(node)[0].tag == tag and not node.text.strip():
            results.append([ead.filename, ead.tree.getpath(node), tag])

    return results

if __name__ == "__main__":
    e = EADDir()
    results = e.characterize_dir(find_nested_tags)

    with open("eads_with_nested_tags.csv", mode="wb") as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerows(result)