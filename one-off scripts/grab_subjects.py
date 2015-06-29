from lxml import etree
import csv
import os
from os.path import join

path = '/Users/BHLStaff/PycharmProjects/vandura/Real_Masters_all'
tags = ['subject', 'corpname', 'geogname', 'persname', 'genreform', 'famname']

for filename in os.listdir(path):
    if filename.endswith(".xml"):
        print ("working on {0}...".format(filename))
        tree = etree.parse(join(path, filename))
        for controlaccess_child in tree.xpath('//controlaccess/*'):
            # print("{0} - {1}".format(controlaccess_child.tag, controlaccess_child.text))
            if any([controlaccess_child.tag in tags for tag in tags]):
                with open('all_subjects.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')

                    if controlaccess_child.text is not None and 'source' in controlaccess_child.attrib:
                        writer.writerow([filename, controlaccess_child.tag, controlaccess_child.text.encode("utf-8"), controlaccess_child.attrib['source'], tree.getpath(controlaccess_child)])
                    elif controlaccess_child.text is not None:
                        writer.writerow([filename, controlaccess_child.tag, controlaccess_child.text.encode("utf-8"), '', tree.getpath(controlaccess_child)])
                    else:
                        continue
