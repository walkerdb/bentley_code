import csv
import re

from extent_splitter_root.extent_parser import split_extents


CHARACTERIZE = False


def characterize_extent(extent):
	number_regex = re.compile(r"(\d\d?\d?\d?\d?\.?\d?\d?)")
	extent = extent.strip(". ")
	extent = re.sub(number_regex, "[n]", extent)
	return extent


def main():
	output = []
	longest_statement = 0
	filename = "all_extents.csv"

	with open(filename, mode="r") as f:
		reader = csv.reader(f)
		unique_item_dict = {}

		for extent_row in reader:
			ead_filename, extent_xpath, extent_statement = extent_row
			extents_split = split_extents(extent_statement)

			if CHARACTERIZE:
				for extent in extents_split:
					extent = characterize_extent(extent)
					unique_item_dict[extent] = unique_item_dict.get(extent, 0) + 1

				if len(extents_split) > longest_statement:
					longest_statement = len(extents_split)
			else:
				for extent in extents_split:
					extent_row.append(extent)
				output.append(extent_row)

		# from itertools import combinations
		#
		# import inflect
		#
		# de_pluralized_set = set()
		# p = inflect.engine()
		#
		# for extent_tuple_1, extent_tuple_2 in combinations(extent_count_list, 2):
		# 	if extent_tuple_1 not in de_pluralized_set:
		# 		print(extent_tuple_1[0])
		# 	comparison = p.compare(extent_tuple_1[0].strip("()"), extent_tuple_2[0].strip("()"))
		# 	if comparison:
		# 		de_pluralized_set.add((extent_tuple_1[0], extent_tuple_1[1] + extent_tuple_2[1]))
		# 		print("found a plural!")
		# 	else:
		# 		de_pluralized_set.add(extent_tuple_1)
		#
		# extent_count_list = sorted(list(de_pluralized_set), key=lambda x: x[0])
		# writer.writerows(extent_count_list)

	# with open("extent_count.csv", mode="wb") as f:
	# 	writer = csv.writer(f)
	# 	extent_count_list = [[key, value] for key, value in unique_item_dict.items()]
	# 	extent_count_list = sorted(extent_count_list, key=lambda x: x[0])
	# 	writer.writerows(extent_count_list)

	with open("extent_split.csv", mode="wb") as f:
		writer = csv.writer(f)
		for row in output:
			if len(row) < longest_statement:
				diff = longest_statement - len(row)
				row = add_blank_elements(row, diff)
			writer.writerow(row)



def add_blank_elements(row, number_of_elements_to_add):

	for i in range(number_of_elements_to_add):
		row.append("")

	return row


if __name__ == "__main__":
	main()