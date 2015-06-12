from extent_parser import split_into_extents
from make_aspace_extent_distinctions import split_into_aspace_components
import csv

def main(source="all_extents.csv"):
	with open(source, mode="r") as f:
		reader = csv.reader(f)

		# we have to reverse the data to ensure xpaths remain accurate while making multiple edits to the same file
		extent_data = [row for row in reversed(list(reader))]

		for filename, xpath, longform_extent_statement in extent_data:
			highlevel_extents = split_into_extents(longform_extent_statement)
			for extent in highlevel_extents:
				aspace_components = split_into_aspace_components(extent)



if __name__ == "__main__":
	main()