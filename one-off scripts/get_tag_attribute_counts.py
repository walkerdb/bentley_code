import os
import csv
from pprint import pprint

from lxml import etree
from tqdm import tqdm


def write_attribute_value_counts(ead_input_dir, tag_name, attribute_name):
    files = [ead for ead in os.listdir(ead_input_dir) if ead.endswith(".xml")]

    values = {}

    for ead in tqdm(files):
        tree = etree.parse(os.path.join(ead_input_dir, ead))
        elements = tree.xpath("//{}".format(tag_name))
        for element in elements:
            value = element.attrib.get(attribute_name, "")
            values[value] = values.get(value, 0) + 1

    with open("{0}_{1}_counts.csv".format(tag_name, attribute_name), mode="wb") as f:
        writer = csv.writer(f)
        header = ["attribute value", "count"]
        value_rows = sorted([[attribute, count] for attribute, count in values.items()])

        writer.writerow(header)
        writer.writerows(value_rows)

    pprint(values)

if __name__ == "__main__":
    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    write_attribute_value_counts(input_dir, tag_name="container", attribute_name="label")
