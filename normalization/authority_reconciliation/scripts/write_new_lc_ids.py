import os
from lxml import etree
from utilities.ead_utilities.ead_utilities import EADDir


def write_new_lc_ids(subjects, input_directory, output_directory):
    ead_dir = EADDir(input_dir=input_directory)
    local_term_map = {(subject[0], subject[1]): (subject[2], subject[3]) for subject in subjects}

    for filename in ead_dir.ead_files:
        tree = etree.parse(os.path.join(input_directory, filename))
        ead_subjects = tree.xpath("//controlaccess/*") + tree.xpath("//origination/*")

        for ead_subject in ead_subjects:
            key = create_tuple_key(ead_subject)

            if key in local_term_map:
                auth_text, auth_link = local_term_map[key]

                create_authfilenumber_attrib(auth_link, ead_subject)
                update_deathdate(auth_text, ead_subject)

        write_ead_to_file(tree, filename, output_directory)


def write_ead_to_file(tree, filename, output_directory):
    with open(os.path.join(output_directory, filename), mode="w") as f:
        f.write(etree.tostring(tree))


def create_authfilenumber_attrib(auth_link, ead_subject):
    if "authfilenumber" in ead_subject.attrib:
        del ead_subject.attrib["authfilnumber"]
    ead_subject.attrib["authfilenumber"] = auth_link


def update_deathdate(auth_text, ead_subject):
    if "persname" in ead_subject.tag and ead_subject.text.strip(".").endswith("-") and not auth_text.endswith("-"):
        ead_subject.text = auth_text


def create_tuple_key(ead_subject):
    subject_term = unicode(ead_subject.text)
    subject_type = unicode(ead_subject.tag)
    return subject_type, subject_term
