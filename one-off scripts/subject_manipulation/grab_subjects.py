import csv
import os
from os.path import join

from lxml import etree
from tqdm import tqdm

# change this to to full path to your own ead folder
path_to_eads = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'

# edit this list to include any other tags whose text you want to normalize
controlaccess_tags = ['subject', 'corpname', 'geogname', 'persname', 'genreform', 'famname']


def build_master_subject_csv():
    with open('all_subjects.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        headers = ['ead', 'controlaccess type', 'controlaccess text', 'controlaccess auth source', 'xpath']
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

                        if 'source' in element.attrib:
                            writer.writerow([filename, element.tag, text, element.attrib['source'], xpath])
                        else:
                            writer.writerow([filename, element.tag, text, '', xpath])

if __name__ == "__main__":
    build_master_subject_csv()
