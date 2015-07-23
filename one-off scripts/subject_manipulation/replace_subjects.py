"""
    Writes new text to a given set of EAD subject tags, with input data taken from a csv file.
    Written to help facilitate subject term normalization.

    Expects csv rows in the form of:
        ead_filename, controlaccess_type, controlaccess_text, controlaccess_auth_source, xpath_to_tag

    Outputs changed files to a given output directory.

    To use, just change the input, output, and csv file paths below, and run the script.
"""


import csv
from os import path

# You'll need to install the two modules below.
# Should be as easy as running "pip install lxml" and "pip install tqdm" from the command-line
from lxml import etree
from tqdm import tqdm

# change these to wherever you would like them to be pointing
# make sure to create the output folder before running the script, or it will crash
input_dir = 'path/to/input/ead/directory'
output_dir = 'path/to/output/directory'
path_to_refined_csv_file = "path/to/csv/data.csv"


def write_refined_text_to_eads():
    with open(path_to_refined_csv_file, mode="r") as f:
        reader = csv.reader(f)
        next(reader)  # skips the header row

        previous_filename = ""
        tree = ""
        edited_filenames = set()

        for filename, tag, text, authority, xpath in tqdm(list(reader)):
            filepath = path.join(input_dir, filename) if filename not in edited_filenames else path.join(output_dir, filename)
    
            # only makes a new root tree and writes the old one to file if the filename listed in the csv has changed
            # this makes things much faster
            if not previous_filename:
                tree = etree.parse(filepath)
            elif filename != previous_filename:
                tree.write(path.join(output_dir, previous_filename), pretty_print=True, xml_declaration=True, encoding="utf-8")
                tree = etree.parse(filepath)

            previous_filename = filename
            replace_subject(tree, filename, text, authority, xpath)
            edited_filenames.add(filename)


def replace_subject(tree, filename, text, authority, xpath):
    subject = tree.xpath(xpath)[0]
    subject.text = text.decode("utf-8")
    if subject.get("source"):
        subject.set("source", authority)

    with open("output/" + filename, mode="w") as f:
        f.write(etree.tostring(tree))

if __name__ == "__main__":
    write_refined_text_to_eads()
