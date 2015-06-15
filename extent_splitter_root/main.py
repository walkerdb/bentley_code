import csv
from os import path
from lxml import etree

from extent_parser import split_into_extents
from make_aspace_extent_distinctions import split_into_aspace_components
import etree_editor



def main(source="all_extents.csv"):
	path_to_eads = r"S:\Curation\Student Work\Walker Boyle\source files\EADs\Master EAD 2015-06-12"
	path_to_output = r"C:\Users\wboyle\PycharmProjects\bentley_code\extent_splitter_root\output"
	edited_filenames = set()

	with open(source, mode="r") as f:
		reader = csv.reader(f)
		reader.next()  # skip the header row

		current_filename = ""
		for filename, xpath, longform_extent_statement in reader:
			# if this file has already been edited, read it from the output directory, not the input directory
			filepath = path.join(path_to_eads, filename) if filename not in edited_filenames else path.join(path_to_output, filename)

			if not current_filename or filename != current_filename:
				tree = etree.parse(filepath)
			current_filename = filename

			parent_xpath = etree_editor.get_c0x_parent_node(filepath, xpath)

			# delete the old extent node
			etree_editor.delete_node(filepath, xpath)

			# split original extent text into component parts
			highlevel_extents = split_into_extents(longform_extent_statement)
			aspace_components = [split_into_aspace_components(extent) for extent in highlevel_extents]

			# write new extent xml to file
			etree_editor.write_aspace_extent_tags(filename, filepath, parent_xpath, aspace_components)

			edited_filenames.add(filename)


if __name__ == "__main__":
	main()