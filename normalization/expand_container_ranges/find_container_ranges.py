from os import listdir, path
from collections import OrderedDict
import csv
import re

from tqdm import tqdm
from lxml import etree


def remove_tags(tag_string):
    tag_regex = r"\<.*?\>"
    tag_string = " ".join(tag_string.split())
    return re.sub(tag_regex, "", tag_string)


def find_container_ranges():
    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    eads_to_skip = ["muschba.xml", "milliken.xml"]
    input_eads = [ead for ead in listdir(input_dir) if ead.endswith(".xml")]

    found_entries = []
    for ead in tqdm(input_eads):
        tree = etree.parse(path.join(input_dir, ead))
        containers = tree.xpath("//container")
        boxnum_count_dict = OrderedDict()

        ead_title = tree.xpath("/ead/archdesc/did/unittitle")[0]
        ead_title = remove_tags(etree.tostring(ead_title))

        for container in containers:
            if container.text:
                if "-" not in container.text:
                    continue

                try:
                    left, right = container.text.split("-")
                    parent_xpath = tree.getpath(container.getparent().getparent().getparent())
                    key = container.text + parent_xpath
                    try:
                        unittitle_text = \
                        tree.xpath(tree.getpath(container.getparent().getparent()) + "/did/unittitle")[0]
                        unittitle_text = remove_tags(etree.tostring(unittitle_text))
                    except:
                        unittitle_text = "failed to grab unittitle text"
                        print("unittitle failure")

                    # checks to see if it's a valid range. Elements on either side of the "-" must be numbers, and
                    # the first number must be greater than the second
                    if is_number(left) and is_number(right) and not any(ead == forbidden_ead for forbidden_ead in eads_to_skip):
                        if int(left) >= int(right):
                            continue

                        boxnum_count_dict[key] = boxnum_count_dict.get(key, [0, ead, ead_title, tree.getpath(container), unittitle_text, container.text])
                        boxnum_count_dict[key][0] += 1

                except ValueError:
                    pass

        # if a particular range appeared multiple times in succession in an ead we can't automate its expansion,
        # so we're only recording the examples that only occur once
        for box_range, data in boxnum_count_dict.items():
            if data[0] == 1:
                found_entries.append(data[1:])

    with open("container_ranges.csv", mode="wb") as f:
        writer = csv.writer(f)
        found_entries = reversed(found_entries)
        writer.writerows(found_entries)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    find_container_ranges()
