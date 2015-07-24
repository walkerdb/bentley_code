import os
import csv
from copy import deepcopy

from lxml import etree


def expand_containers(ead_path, xpaths):
	tree = etree.parse(ead_path)
	for xpath, text in xpaths:
		node = tree.xpath(xpath)[0]
		parent = node.getparent()
		left, right = map(int, text.split("-"))
		index = parent.getchildren().index(node)

		new_node = deepcopy(node.getparent().getparent())
		for i in range(left, right + 1):
			pass



def load_data(input_filepath):
	data_dict = {}
	with open(input_filepath, mode="r") as f:
		reader = csv.reader(f)
		for ead, xpath, text in reader:
			data_dict[ead] = data_dict.get(ead, [])
			data_dict[ead].append([xpath, text])
	return data_dict

if __name__ == '__main__':
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	data_dict = load_data("container_ranges.csv")

	for ead, xpaths in data_dict.items():
		ead_path = os.path.join(input_dir, ead)
		expand_containers(ead_path, xpaths)
