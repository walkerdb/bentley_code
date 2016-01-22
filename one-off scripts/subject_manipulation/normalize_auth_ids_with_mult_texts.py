import csv
import os
from lxml import etree
from ead_utilities import EADDir, EAD


def load_data(filename):
    with open(filename, mode="rb") as f:
        data = []
        reader = csv.DictReader(f)

        for dct in reader:
            data.append(dct)

        return data


def replace_subjects(ead):
    dict_list = load_data("normalization data.csv")
    tags = ead.tree.xpath("//controlaccess/*") + ead.tree.xpath("//origination/*")

    for dct in dict_list:
        for tag in tags:
            tag.text = tag.text.strip()

            texts = [dct["tag 1"], dct["tag 2"], dct["tag 3"], dct["tag 4"]]
            texts = [text.split(": ", 1) for text in texts if text]

            for text in texts:
                if text[0] == tag.tag and text[1] == tag.text and tag.get("authfilenumber"):
                    index = dct["normalize to"]

                    # deleting authfilenumbers if the normalization index is "x"
                    if index == "x":
                        if tag.text == "University of Michigan.":
                            continue

                        del tag.attrib["authfilenumber"]
                        continue

                    # normalizing terms
                    normal_form = texts[int(index) - 1]
                    normal_tag = normal_form[0]
                    normal_text = normal_form[1]

                    tag.tag = normal_tag
                    tag.text = normal_text




if __name__ == "__main__":
    directory = r'C:\Users\wboyle\PycharmProjects\without-reservations\Real_Masters_all'
    ead_dir = EADDir(input_dir=directory)
    data = load_data("normalization data.csv")

    ead_dir.apply_function_to_dir(replace_subjects, output_dir=directory)
