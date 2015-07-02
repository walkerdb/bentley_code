import csv
import os
from os import path
from lxml import etree
from tqdm import tqdm

input_dir = "/Users/BHLStaff/PycharmProjects/vandura/Real_Masters_all"
output_dir = "output/"

def main():
    with open("all_subjects_refined_reversed.csv", mode="r") as f:
        reader = csv.reader(f)
        previous_filename = ""
        tree = ""
        edited_filenames = set()

        for filename, tag, text, authority, xpath in tqdm(list(reader)):
            filepath = path.join(input_dir, filename) if filename not in edited_filenames else path.join(output_dir, filename)
    
            # only make a new root tree and write the old one to file if the filename has changed
            if not previous_filename:
                tree = etree.parse(filepath)
            elif filename != previous_filename:
                try:
                    tree.write(path.join(output_dir, previous_filename), pretty_print=True)
                except AttributeError:
                    print(type(tree) + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                tree = etree.parse(filepath)
            previous_filename = filename

            replace_subject(tree, filename, text, authority, xpath)


def replace_subject(tree, filename, text, authority, xpath):
    subject = tree.xpath(xpath)[0]
    subject.text = text.decode("utf-8")
    if subject.get("source"):
        subject.set("source", authority)

    # print(etree.tostring(subject))

    with open("output/" + filename, mode="w") as f:
        f.write(etree.tostring(tree))

if __name__ == "__main__":
    main()