from os import listdir, path
from collections import OrderedDict
import csv

from tqdm import tqdm
from lxml import etree

def find_container_ranges():
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	eads_to_skip = ["muschba.xml", ]
	input_eads = [ead for ead in listdir(input_dir) if ead.endswith(".xml")]

	found_entries = []
	for ead in tqdm(input_eads):
		tree = etree.parse(path.join(input_dir, ead))
		containers = tree.xpath("//container")
		boxnum_count_dict = OrderedDict()

		for container in containers:
			if container.text:
				if "-" in container.text:
					try:
						left, right = container.text.split("-")
						parent_xpath = tree.getpath(container.getparent().getparent().getparent())
						key = container.text + parent_xpath

						# checks to see if it's a valid range. Elements on either side of the "-" must be numbers, and
						# the first number must be greater than the second
						if is_number(left) and is_number(right) and not any(ead == forbidden_ead for forbidden_ead in eads_to_skip):
							if int(left) < int(right):
								boxnum_count_dict[key] = boxnum_count_dict.get(key, [0, ead, tree.getpath(container), container.text])
								boxnum_count_dict[key][0] += 1

					except ValueError:
						pass

		# if a particular range appeared multiple times in succession in an ead we can't automate its expansion,
		# so we're only recording the examples that only occur once
		for box_range, data in boxnum_count_dict.items():
			if data[0] == 1:
				found_entries.append(data[1:])

	with open("container_ranges.csv", mode="wb") as f:
		writer = csv.writer(f)
		found_entries = reversed(found_entries)
		writer.writerows(found_entries)


def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	find_container_ranges()
