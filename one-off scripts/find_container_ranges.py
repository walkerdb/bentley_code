from os import listdir, path
import csv

from tqdm import tqdm
from lxml import etree

input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'

eads = [ead for ead in listdir(input_dir) if ead.endswith(".xml")]

found_entries = []
for ead in tqdm(eads):
	tree = etree.parse(path.join(input_dir, ead))
	containers = tree.xpath("//container")
	for container in containers:
		if container.text:
			if "-" in container.text:
				found_entries.append([ead, tree.getpath(container), container.text])

with open("box_ranges.csv", mode="wb") as f:
	writer = csv.writer(f)
	writer.writerows(found_entries)