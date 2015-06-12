import csv
import re

from extent_splitter_root.extent_parser import split_into_separate_extents


CHARACTERIZE = False


def main():
	output = []
	longest_statement = 0
	filename = "all_extents.csv"

	with open(filename, mode="r") as f:
		reader = csv.reader(f)
		reader.next()  # skip the header row

		for extent_row in reader:
			ead_filename, extent_xpath, extent_statement = extent_row
			extents_split = split_into_separate_extents(extent_statement)

			for extent in extents_split:
				extent_row.append(extent)
			output.append(extent_row)

			if len(extents_split) > longest_statement:
				longest_statement = len(extents_split)

	with open("extent_split.csv", mode="wb") as f:
		writer = csv.writer(f)

		header = ["EAD filename", "XPath to extent", "Original extent text"]
		for i in range(longest_statement):
			header.append("split extent segment {}".format(i + 1))
		writer.writerow(header)

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