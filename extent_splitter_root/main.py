import csv
from os import path

from extent_parser import split_into_extents
from make_aspace_extent_distinctions import split_into_aspace_components
import etree_editor



def main(source="all_extents.csv"):
	path_to_eads = r"S:\Curation\Student Work\Walker Boyle\source files\EADs\Master EAD 2015-06-12"
	path_to_output = r"S\Curation\Student Work\Walker Boyle\extent_fix_output"
	edited_filenames = set()

	with open(source, mode="r") as f:
		reader = csv.reader(f)
		reader.next()  # skip the header row

		for filename, xpath, longform_extent_statement in reader:
			filepath = path.join(path_to_eads, filename) if filename not in edited_filenames else path.join(path_to_output, filename)
			parent_xpath = etree_editor.get_c0x_parent_node(filepath, xpath)

			# print(filename)
			etree_editor.delete_node(filepath, xpath)

			highlevel_extents = split_into_extents(longform_extent_statement)
			for extent in highlevel_extents:
				aspace_components = split_into_aspace_components(extent)
				etree_editor.write_aspace_extent_tags(filepath, parent_xpath, aspace_components)

				# keep writing this!


if __name__ == "__main__":
	main()