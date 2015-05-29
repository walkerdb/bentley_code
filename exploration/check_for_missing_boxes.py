'''
Checks each ead file in a given directory to see whether the finding-aid is missing any boxes.
Loops through every possible integer between the lowest and highest box numbers appearing in the EAD file, and
writes to a file if it discovers anything missing.
'''

# standard library imports
from string import ascii_letters
from operator import itemgetter
from itertools import groupby
from os import listdir
import csv

# custom library imports - these will need to be manually installed on your system for the script to work
# command-line commands to install:
## pip install lxml
## pip install naturalsort
from lxml import etree
from natsort import natsort


def main():
	path_to_eads_to_check = "/some/path"  # change this string to your input directory path

	container_xpath = "//container"

	# check every file in the file list
	files = []
	for filename in listdir(path_to_eads_to_check):
		if filename.endswith(".xml"):
			files.append(filename)

	for file in files:
		print("Checking {0}...".format(file))
		root_tree = etree.parse(path_to_eads_to_check + "/" + file)
		boxes = set()
		has_letters = False

		# grab all containers in the EAD file
		containers = root_tree.xpath(container_xpath)

		# for every box in the EAD, add its box number to a set of unique numbers
		for container in containers:
			type = container.get("type")
			text = container.text

			if type == "box":  # we only want containers that are boxes
				if text is None:  # check if the box number is empty
					write_to_csv_file("eads_with_empty_box_numbers.csv", [file, root_tree.getpath(container)])
				else:
					# check if there are any non-numeric characters in the box number
					if all(letter not in text for letter in ascii_letters):
						if "-" in text:  # if there is a "-" in the number, it is a range of numbers, which we need to expand
							num_range = text.split("-")
							num_start = int(num_range[0])
							try:  # sometimes a number only has a trailing "-", in which case we need to catch the resulting index error
								num_end = int(num_range[1])
							except:
								num_end = num_start

							for box_num in range(num_start, num_end + 1):
								boxes.add(box_num)
						else:  # if the number is not a range, cast the string to an int and proceed normally
							try:
								boxes.add(int(text))
							except:  # if the string to int conversion fails, some other non-alphanumeric character in the box number
								write_to_csv_file("eads_with_unusual_box_numbers.csv", [file, root_tree.getpath(container), text])
					else:
						has_letters = True
						boxes.add(text)

		# now that all box numbers have been accounted for, see if any are missing from the expected sequential order
		if len(boxes) == 0:  # ead has no boxes to check
			write_to_csv_file("eads_with_no_boxes.csv", [file])
		elif has_letters:  # box numbers contain non-numeric characters, so cannot be checked
			print("Box numbers have non-numeric characters")
			write_to_csv_file("eads_with_ascii_in_box_numbers.csv", [file])
		else:  # if the ead has boxes, and none of its box numbers have letters in them, check the box list for missing numbers
			missing_numbers = get_missing_numbers(boxes)
			if len(missing_numbers) > 0:
				message = "Missing the following box numbers: {0}".format(", ".join(missing_numbers))
				write_to_csv_file("eads_with_missing_boxes.csv", [file, message])


def get_missing_numbers(list_or_set):
	# set the maximum and minimum box numbers found in the given box-number list
	min_number = min(list_or_set)
	max_number = max(list_or_set)

	missing_numbers = []

	# for each integer between the minimum and maximum value, check if that integer is in the box list.
	# If it does not, that box is missing.
	i = min_number
	while i < max_number:
		if i not in list_or_set:
			missing_numbers.append(i)
		i += 1

	# sort the list of missing numbers
	missing_numbers.sort()

	# In some cases there are hundreds of "missing" boxes. To make the output more human-readable, the code below contracts
	# sequential series of missing numbers into a range, e.g. [1, 2, 3, 4] into "1-4"

	# First extract each series of sequential numbers
	# (code from the python docs, see https://docs.python.org/2.6/library/itertools.html#examples)
	range_lists = []
	for k, g in groupby(enumerate(missing_numbers), lambda ix: ix[0]-ix[1]):
		range_lists.append(map(itemgetter(1), g))

	# make each sequence human-readable, by grabbing the first and last values of each sequence list
	ranges = []
	for range in range_lists:
		if len(range) > 1:
			ranges.append("{0}-{1}".format(range[0], range[-1]))
		elif len(range) == 1:
			ranges.append(str(range[0]))

	# Since this is a list of strings that sometimes contain non-numeric characters, we use the naturalsort library to
	# return the results in the expected order.
	return natsort(ranges)


def write_to_csv_file(log_filename, row_to_write):
	with open(log_filename, mode="ab") as f:
		writer = csv.writer(f)
		writer.writerow(row_to_write)


if __name__ == "__main__":
	main()