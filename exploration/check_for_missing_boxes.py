# standard library imports
from string import ascii_letters
from operator import itemgetter
from itertools import groupby
from os import listdir
import csv

# custom library imports
from lxml import etree
from natsort import natsort


def main():
	path_to_eads_to_check = "S:/Curation/Projects/Mellon/ArchivesSpace/ATeam_Migration/EADs/Real_Masters_all"
	container_xpath = "//container"

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

		for container in containers:
			type = container.get("type")
			text = container.text

			if type == "box":  # we only want containers that are boxes
				if text is None:  # check if the box number is empty
					write_to_file("eads_with_empty_box_numbers.csv", file, root_tree.getpath(container))
				else:
					# check if there are any non-numeric characters in the box number
					if all(letter not in text for letter in ascii_letters):
						if "-" in text:  # if there is a "-" in the number, it is a range of numbers, which we need to expand
							num_range = text.split("-")
							num_start = int(num_range[0])

							try:  # sometimes a number only has a trailing "-", in which case we need to catch the index error
								num_end = int(num_range[1])
							except:
								num_end = num_start

							for box_num in range(num_start, num_end + 1):
								boxes.add(box_num)
						else:  # if the number is not a range, cast the string to an int and proceed normally
							try:  # if the string to int conversion fails, there is some other non-alphanumerical character in the box number
								boxes.add(int(text))
							except:
								write_to_file("eads_with_unusual_box_numbers.csv", file, "something wonky at {0}. Text was {1}".format(root_tree.getpath(container), text))
					else:
						has_letters = True
						boxes.add(text)

		if len(boxes) == 0:
			print("{0} has no boxes.\n".format(file))
			write_to_file("eads_with_no_boxes.csv", file)
		elif has_letters:
			print("Box numbers have non-numeric characters")
			write_to_file("eads_with_ascii_in_box_numbers.csv", file)
		else:
			# if the ead has boxes, and none of its box numbers have letters in them, check the box list for missing numbers
			missing_numbers = get_missing_numbers(boxes)
			if len(missing_numbers) > 0:
				message = "Missing the following box numbers: {0}".format(", ".join(missing_numbers))
				write_to_file("eads_with_missing_boxes.csv", file, message)

def write_to_file(log_filename, name_of_file_with_error, message=""):
	with open(log_filename + ".csv", mode="ab") as f:
		writer = csv.writer(f)
		writer.writerow([name_of_file_with_error, message])


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
	for k, g in groupby(enumerate(missing_numbers), lambda (j, x): j-x):
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


if __name__ == "__main__":
	main()