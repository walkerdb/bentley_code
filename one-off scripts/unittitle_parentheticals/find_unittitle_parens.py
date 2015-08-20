import os
import re
import csv

from lxml import etree
from tqdm import tqdm

def find_parens(input_dir):
	output = []
	tag_regex = r"\<\/?.*?\>"

	eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
	for ead in tqdm(eads):
		tree = etree.parse(os.path.join(input_dir, ead))
		titles = tree.xpath("//unittitle")
		for title in titles:
			text = etree.tostring(title).strip()
			if "(" in text or "[" in text:
				xpath = tree.getpath(title)
				text_without_xml = re.sub(tag_regex, "", text).strip()
				parenthetical = re.search(r'([\(\[].*?[\)\]])', text_without_xml)
				parenthetical = parenthetical.group(1) if parenthetical else ""
				if parenthetical.strip("()[] 1234567890"):
					if parenthetical.strip("()[] ")[0].isdigit() \
						and not re.search(r"\d{4}|\dth|\dst|\dnd|\d,\d{3}|\-[A-Z]\)|\d[A-Z]", parenthetical) \
						and "/" not in parenthetical:

						output.append([ead, xpath, text_without_xml, parenthetical, text])

	with open("possible_extents.csv", mode="wb") as f:
		writer = csv.writer(f)
		writer.writerows(output)

if __name__ == "__main__":
	input_dir = r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all"
	find_parens(input_dir)
