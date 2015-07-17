from os import listdir, path
import csv

from tqdm import tqdm
from lxml import etree

def find_container_ranges():
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'

	eads = [ead for ead in listdir(input_dir) if ead.endswith(".xml")]

	found_entries = []
	for ead in tqdm(eads):
		tree = etree.parse(path.join(input_dir, ead))
		containers = tree.xpath("//container")
		for container in containers:
			if container.text:
				if "-" in container.text:
					try:
						left, right = container.text.split("-")
						if is_number(left) and is_number(right):
							found_entries.append([ead, tree.getpath(container), container.text])
					except ValueError:
						pass

	with open("box_ranges.csv", mode="wb") as f:
		writer = csv.writer(f)
		writer.writerows(found_entries)


def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	find_container_ranges()
