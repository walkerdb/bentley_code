import os
from pprint import pprint

from lxml import etree
from tqdm import tqdm


def main(input_dir):
	files = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]

	analogs = {}

	for ead in tqdm(files):
		tree = etree.parse(os.path.join(input_dir, ead))
		extents = tree.xpath("//extent")
		for extent in extents:
			analog = extent.attrib.get("encodinganalog", "")
			analogs[analog] = analogs.get(analog, 0) + 1

	pprint(analogs)

if __name__ == "__main__":
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	main(input_dir)
