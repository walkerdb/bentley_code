"""
    Reads through a folder of input EADs and writes a list of every subject term appearing under a <controlaccess> or
    <origination> tag. Written to help facilitate subject term normalization.

    Row format of the output csv file:
        ead_filename, controlaccess_type, controlaccess_text, controlaccess_auth_source, xpath_to_tag

    To use, just change the ead path below and run the script. An output file will appear in whichever directory you
    ran the script from.
"""

import csv
import os
from os.path import join

# You'll need to install the two modules below. lxml processes the xml, and tqdm gives a command-line progress bar
# Should be as easy as running "pip install lxml" and "pip install tqdm" from the command-line
from lxml import etree
from tqdm import tqdm

# change this to to full path to your own ead folder
path_to_eads = r'C:\Users\wboyle\PycharmProjects\without-reservations\Real_Masters_all'

# edit this list to include any other tags whose text you want to capture
controlaccess_tags = ['subject', 'corpname', 'geogname', 'persname', 'genreform', 'famname']


def build_master_subject_csv():
    with open('all_subjects_new.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        headers = ['ead', 'type', 'text', 'auth id', 'auth source', 'xpath']
        writer.writerow(headers)

        for filename in tqdm([ead for ead in os.listdir(path_to_eads) if ead.endswith(".xml")]):
            tree = etree.parse(join(path_to_eads, filename))
            controlaccess_children = tree.xpath("//controlaccess/*")
            origination_children = tree.xpath("//origination/*")
            elements_to_look_through = controlaccess_children + origination_children

            for element in elements_to_look_through:
                if any([element.tag == controlaccess_tag for controlaccess_tag in controlaccess_tags]):
                    if element.text is not None:
                        text = element.text.encode("utf-8")  # the encode call is necessary for text with special characters
                        xpath = tree.getpath(element)
                        id = element.get("authfilenumber", "")
                        source = element.get("source", "")
                        writer.writerow([filename, element.tag, text, id, source, xpath])

if __name__ == "__main__":
    build_master_subject_csv()
