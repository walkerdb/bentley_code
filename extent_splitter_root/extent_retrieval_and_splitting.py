import csv
import re

from extent_splitter_root import extent_splitter


CHARACTERIZE = True


def main():
	output = []
	longest_statement = 0
	filename = "all_extents.csv"
	print(filename)
	number_regex = re.compile(r"(\d\d?\d?\d?\d?\.?\d?\d?)")
	beginning_num_regex = re.compile(r"^\(?\[?\d\d?\d?\d?.?\d?\d? ")
	with open(filename, mode="r") as f:
		reader = csv.reader(f)
		unique_item_dict = {}
		for extent_row in reader:
			ead_filename = extent_row[0]
			extent_xpath = extent_row[1]
			extent_statement = extent_row[2]
			split_extents = extent_splitter.split_extents(extent_statement)
			row = [ead_filename, extent_xpath, extent_statement]

			if CHARACTERIZE:
				for extent in split_extents:
					extent = re.sub(beginning_num_regex, "", extent)
					extent = extent.strip("()[]. ")
					extent = re.sub(number_regex, "[x]", extent)

					# add count for characterized version
					unique_item_dict[extent] = unique_item_dict.get(extent, 0) + 1

				# 	row.append(extent.strip(" .1234567890"))
				# output.append(row)

				# keeping track of the longest line in the csv, so that we can add
				if len(split_extents) > longest_statement:
					longest_statement = len(split_extents)
			else:
				row.append(split_extents)
				output.append(row)

	with open("extent_count.csv", mode="w", newline="") as f:
		writer = csv.writer(f)
		list_ = []
		for key, value in unique_item_dict.items():
			list_.append([key, value])

		list_ = sorted(list_, key=lambda x: x[0])
		writer.writerows(list_)
		exit()


	with open("split_extents.csv", mode="w", newline="") as f:
		writer = csv.writer(f)
		if CHARACTERIZE:
			for row in output:
				if len(row) < longest_statement:
					diff = longest_statement - len(row)
					row = add_blank_elements(row, diff)
				writer.writerow(row)
		else:
			writer.writerows(output)


def add_blank_elements(row, number_of_elements_to_add):
	i = 0
	while i < number_of_elements_to_add:
		row.append("")
		i += 1

	return row


if __name__ == "__main__":
	main()