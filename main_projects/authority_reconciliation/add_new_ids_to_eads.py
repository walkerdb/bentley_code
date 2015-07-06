import csv
import os

from lxml import etree
from tqdm import tqdm

def write_ids_to_ead(auth_dict, input_dir, output_dir):
    tags = ['subject', 'corpname', 'geogname', 'persname', 'genreform', 'famname']
    eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]

    for ead in tqdm(eads):
        tree = etree.parse(os.path.join(input_dir, ead))

        for controlaccess_child in tree.xpath('//controlaccess/*'):
            if any([controlaccess_child.tag in tag for tag in tags]):
                if controlaccess_child.text in auth_dict:
                    controlaccess_child.attrib['authfilenumber'] = auth_dict[controlaccess_child.text]

        with open(os.path.join(output_dir, ead), mode="w") as f:
            f.write(etree.tostring(tree))


if __name__ == "__main__":
    with open("geogname_id_dict.txt", mode="r") as f:
        auth_dict = eval(f.read())

    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    output_dir = r'c:\Users\wboyle\PycharmProjects\bentley_code\main_projects\authority_reconciliation\output'

    write_ids_to_ead(auth_dict, input_dir, output_dir)