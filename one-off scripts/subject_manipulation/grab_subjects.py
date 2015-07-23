import csv
import os
from os.path import join

from lxml import etree

# change this to to full path to your own ead folder
path_to_eads = 'path/to/your/eads'

# edit this list to include any other tags whose text you want to normalize
controlaccess_tags = ['subject', 'corpname', 'geogname', 'persname', 'genreform', 'famname']


def build_master_subject_csv():
    with open('all_subjects.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')

        for filename in [ead for ead in os.listdir(path_to_eads) if ead.endswith(".xml")]:
            tree = etree.parse(join(path_to_eads, filename))
            for tag in controlaccess_tags:
                for result in tree.xpath("//{0}".format(tag)):
                    if result.text is not None:
                        text = result.text.encode("utf-8")  # the encode call is necessary for text with special characters
                        xpath = tree.getpath(result)

                        if 'source' in result.attrib:
                            writer.writerow([filename, tag, text, result.attrib['source'], xpath])
                        else:
                            writer.writerow([filename, tag, text, '', xpath])

if __name__ == "__main__":
    build_master_subject_csv()

