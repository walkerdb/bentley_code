import csv
from os import path

from lxml import etree

# change these to your wherever you would like them to be pointing
input_dir = "path/to/master/eads"
output_dir = "path/to/output/folder"
path_to_refined_csv_file = "path/to/csv_data.csv"


def write_refined_text_to_eads():
    with open(path_to_refined_csv_file, mode="r") as f:
        reader = csv.reader(f)
        previous_filename = ""
        tree = ""
        edited_filenames = set()

        for filename, tag, text, authority, xpath in reader:
            filepath = path.join(input_dir, filename) if filename not in edited_filenames else path.join(output_dir, filename)
    
            # only make a new root tree and write the old one to file if the filename listed in the csv has changed
            # this makes things much faster
            if not previous_filename:
                tree = etree.parse(filepath)
                print("Working on {0}...".format(filename))
            elif filename != previous_filename:
                tree.write(path.join(output_dir, previous_filename), pretty_print=True)
                tree = etree.parse(filepath)
                print("Working on {0}...".format(filename))

            previous_filename = filename
            replace_subject(tree, filename, text, authority, xpath)


def replace_subject(tree, filename, text, authority, xpath):
    subject = tree.xpath(xpath)[0]
    subject.text = text.decode("utf-8")
    if subject.get("source"):
        subject.set("source", authority)

    with open("output/" + filename, mode="w") as f:
        f.write(etree.tostring(tree))

if __name__ == "__main__":
    write_refined_text_to_eads()
