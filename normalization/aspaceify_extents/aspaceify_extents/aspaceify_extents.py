from __future__ import absolute_import
from collections import defaultdict
from os import path
import csv

from lxml import etree
from tqdm import tqdm
from normalization.aspaceify_extents.aspaceify_extents.scripts.etree_editor import add_new_physdescs_to_tree

from .scripts.make_aspace_extent_distinctions import split_into_aspace_components
from .scripts.prettifydirectory import prettify_xml_in_directory
from .scripts.extent_parser import split_into_extents
from .scripts import etree_editor
from utilities.ead_utilities.ead_utilities import EAD


def main(extent_list, input_dir, output_dir):

    edited_filenames = set()
    types = {}

    previous_filename = ""

    # initialize errors csv
    with open("extents_with_errors.csv", mode="ab") as f:
        pass

    new_physdescs = defaultdict(list)
    for filename, xpath, longform_extent_statement in tqdm(extent_list, desc="splitting, parsing, and writing extents...", leave=True):

        # if this file has already been edited, read it from the output directory, not the input directory
        filepath = path.join(input_dir, filename) if filename not in edited_filenames else path.join(output_dir, filename)

        # only make a new root tree and write the old one to file if the filename has changed
        if not previous_filename:
            ead = EAD(filepath)
        elif filename != previous_filename:
            add_new_physdescs_to_tree(ead.tree, new_physdescs)
            new_physdescs = defaultdict(list)
            ead.prettyprint(output_dir)
            ead = EAD(filepath)
        previous_filename = filename

        try:
            # find the xpath of the extent's parent
            parent_of_physdesc_xpath = etree_editor.get_parent_node(ead.tree, xpath)

            physdesc = ead.tree.xpath(xpath)[0].getparent()
            portion = physdesc.get("altrender", "")

            # split original extent text into component parts
            highlevel_extents = split_into_extents(longform_extent_statement)
            is_multiple_extents = True if len(highlevel_extents) > 1 else False
            aspace_components = [split_into_aspace_components(extent, physdesc, portion, is_multiple_extents) for extent in highlevel_extents]


            # create_new_physdesc
            new_physdesc = etree_editor.make_aspace_formatted_physdesc(aspace_components)

            if len(new_physdesc) == 0:
                continue

            new_physdescs[parent_of_physdesc_xpath].append(new_physdesc)

            # remove the old physdesc
            physdesc.getparent().remove(physdesc)

            edited_filenames.add(filename)

            # temp code to get list of all types in collection
            for aspace_component in aspace_components:
                type_ = aspace_component.type_.strip(" ")
                type_ = type_.lstrip("1234567890.- ")
                # type_ = type_.strip(""" .;:()-"'""")
                types[type_] = types.get(type_, 0) + 1

        except (IndexError, ValueError) as e:
            with open("extents_with_errors.csv", mode="ab") as f:
                writer = csv.writer(f)
                writer.writerow([filename, xpath, longform_extent_statement, str(e)])
            continue

    # clean up the changes
    prettify_xml_in_directory(input_dir=output_dir, output_dir=output_dir, eads=tuple(edited_filenames))

    with open("all_types.csv", mode="wb") as f:
        writer = csv.writer(f)
        rows = [[key, value] for key, value in types.items()]
        rows.sort(key=lambda x: -x[1])
        writer.writerows(rows)


if __name__ == "__main__":
    main()