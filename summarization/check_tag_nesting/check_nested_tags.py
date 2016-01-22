import csv

from utilities.ead_utilities.ead_utilities import EADDir

def main():
    input_directory = "path/to/your/ead/files"

    e = EADDir(input_directory)
    results = e.characterize_dir(find_nested_tags)

    with open("eads_with_nested_tags.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerow(["ead file name", "xpath to self-nested tag", "tag type"])
        for result in results:
            writer.writerows(result)


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
    main()
