import os
from lxml import etree
from utilities import EADDir


def write_new_lc_ids(subjects, input_directory, output_directory):
    ead_dir = EADDir(input_dir=input_directory)
    local_term_map = {(subject[0], subject[1]): subject[2] for subject in subjects}

    terms = ["geogname", "persname", "corpname"]

    for filename in ead_dir.ead_files:
        tree = etree.parse(os.path.join(filename, input_directory))

        ead_subjects = tree.xpath("//controlaccess/*") + tree.xpath("//origination/*")

        for ead_subject in ead_subjects:
            subject_term = unicode(ead_subject.text)
            subject_type = unicode(ead_subject.tag)
            key = (subject_type, subject_term)

            if key in local_term_map:
                ead_subject.text = local_term_map[key]
                # TODO erm... I need to go back and add the LC identifier links to the subjects data structure.
                pass
