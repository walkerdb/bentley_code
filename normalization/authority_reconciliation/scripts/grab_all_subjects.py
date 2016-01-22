import os

from lxml import etree
from tqdm import tqdm

from utilities.ead_utilities.ead_utilities import EADDir


def grab_all_subjects(ead_directory_path):
    ead_dir = EADDir(input_dir=ead_directory_path)
    subjects = set()

    for ead in tqdm(ead_dir.ead_files, desc="extracting all unique subjects from EAD files..."):
        tree = etree.parse(os.path.join(ead_dir.input_dir, ead))
        subjects = subjects.union(grab_all_subjects_from_etree(tree))

    return subjects


def grab_all_subjects_from_etree(tree):
    terms = ["persname", "corpname", "geogname"]
    names = set()
    for term in terms:
        tags = tree.xpath("//controlaccess/{}".format(term)) + tree.xpath("//origination/{}".format(term))
        for tag in tags:
            name = unicode(tag.text)
            names.add((name, unicode(term)))

    return names

