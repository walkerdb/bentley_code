import os

from lxml import etree
from tqdm import tqdm

import extent_constants


def replace_extent_nums_in_dir(input_directory):
	eads = [ead for ead in os.listdir(input_directory) if ead.endswith(".xml")]

	for ead in tqdm(eads):
		try:
			tree = etree.parse(os.path.join(input_directory, ead))
		except etree.XMLSyntaxError:
			print(ead)
			exit()
		extents = tree.xpath("//extent")
		for extent in extents:
			try:
				extent.text = replace_written_numbers_with_digits(extent.text.encode("utf-8")).decode("utf-8")
			except AttributeError:
				print(etree.tostring(extent))
		with open("output/{0}".format(ead), mode="w") as f:
			f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))


def replace_written_numbers_with_digits(extent):
	written_numbers_dict = extent_constants.numbers_dict
	extent = " {} ".format(extent)

	extent = extent.replace("(", "( ")
	extent = extent.replace("[", "[ ")

	for key, value in written_numbers_dict.items():
		if key in extent:
			extent = extent.replace(key, " {0} ".format(value))

	extent = extent.replace("(  ", "(")
	extent = extent.replace("( ", "(")
	extent = extent.replace("[ ", "[")

	return extent.strip()

if __name__ == "__main__":
	input_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	replace_extent_nums_in_dir(input_directory)