from __future__ import absolute_import
from os import path
import csv

from lxml import etree
from tqdm import tqdm

from .scripts.make_aspace_extent_distinctions import split_into_aspace_components
from .scripts.prettifydirectory import prettify_xml_in_directory
from .scripts.extent_parser import split_into_extents
from .scripts import etree_editor


def main(source="C:/Users/wboyle/PycharmProjects/bentley_code/aspaceify_extents/input/all_extents_reversed.csv"):
	path_to_eads = "S:/Curation/Student Work/Walker Boyle/source files/EADs/Master EAD 2015-06-12"
	path_to_output = "C:/Users/wboyle/PycharmProjects/bentley_code/aspaceify_extents/output"
	edited_filenames = set()

	with open(source, mode="r") as f:
		reader = csv.reader(f)
		reader.next()  # skip the header row

		previous_filename = ""
		tree = ""
		for filename, xpath, longform_extent_statement in tqdm(list(reader), desc="Extent parsing progress", leave=True):
			# if this file has already been edited, read it from the output directory, not the input directory
			filepath = path.join(path_to_eads, filename) if filename not in edited_filenames else path.join(path_to_output, filename)

			# only make a new root tree and write the old one to file if the filename has changed
			if not previous_filename:
				tree = etree.parse(filepath)
			elif filename != previous_filename:
				try:
					tree.write(path.join(path_to_output, previous_filename), pretty_print=True)
				except AttributeError:
					print(type(tree) + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				tree = etree.parse(filepath)
			previous_filename = filename

			try:
				# find the xpath of the extent's parent
				parent_xpath = etree_editor.get_parent_node(tree, xpath)

				# delete the old extent node
				tree = etree_editor.delete_node(tree, xpath)

				# split original extent text into component parts
				highlevel_extents = split_into_extents(longform_extent_statement)
				aspace_components = [split_into_aspace_components(extent) for extent in highlevel_extents]

				# write new extent xml to file
				tree = etree_editor.write_aspace_extent_tags(filename, tree, parent_xpath, aspace_components)

				edited_filenames.add(filename)

			except:
				with open("extent_fix_errors.csv", mode="ab") as f:
					writer = csv.writer(f)
					writer.writerow([filename, xpath, longform_extent_statement])
				continue

	# clean up the changes
	prettify_xml_in_directory(input_dir=path_to_output, output_dir=path_to_output)


if __name__ == "__main__":
	main()