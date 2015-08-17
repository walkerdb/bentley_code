import csv
import os
import re
import math
import random
from copy import deepcopy
from collections import defaultdict

from lxml import etree
from tqdm import tqdm

def grab_suspects(input_dir):
	eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
	tag_regex = r"\<\/?.*?\>"

	data = []
	for ead in tqdm(eads):
		tree = etree.parse(os.path.join(input_dir, ead))
		unittitles = tree.xpath("//unittitle")
		for unittitle in unittitles:
			if is_suspect(unittitle):
				text_with_tags = " ".join(etree.tostring(unittitle).split()).strip()
				text_without_tags = " ".join(re.sub(tag_regex, "", text_with_tags).split()).strip()
				data.append([ead, tree.getpath(unittitle), text_with_tags, text_without_tags])

	with open('wonky_unitdate_display_candidates.csv', mode="wb") as f:
		writer = csv.writer(f)
		writer.writerows(data)
		print(len(data))

def fix_suspects(input_dir):
	with open("wonky_unitdate_display_candidates.csv", mode="r") as f:
		example_dict = {}
		reader = csv.reader(f)
		items = list(reader)
		items.reverse()
		for filename, xpath, text_with_tags, text_without_tags in tqdm(items):
			example_dict[filename] = example_dict.get(filename, [])
			example_dict[filename].append(xpath)

		for ead, xpaths in tqdm(example_dict.items()):
			tree = etree.parse(os.path.join(input_dir, ead))
			for xpath in xpaths:
				unittitle = tree.xpath(xpath)[0]
				unittitle = move_unitdates(unittitle)

			with open(os.path.join("output", ead), mode="w") as f:
				f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))


def is_suspect(unittitle):
	unitdates = unittitle.xpath("unitdate")
	is_suspect_unittitle = False
	if len(unitdates) > 1:
		for unitdate in unitdates:
			if unitdate.tail:
				if len(unitdate.tail.strip(", 1234567890-")) > 5:
					is_suspect_unittitle = True

	return is_suspect_unittitle


def move_unitdates(unittitle_node):
	parent = unittitle_node.getparent()
	unitdates = unittitle_node.xpath("unitdate")

	copies = []
	for unitdate in unitdates:
		copies.append(deepcopy(unitdate))

	tag_regex = r"<unitdate.*?>(.*?)<\/unitdate>"
	new_node = etree.fromstring(re.sub(tag_regex, '\g<1>', etree.tostring(unittitle_node)))

	parent.insert(parent.index(unittitle_node), new_node)
	parent.remove(unittitle_node)
	for copy in copies:
		copy.tail = ""
		parent.insert(parent.index(new_node) + 1, copy)

	return parent.xpath("unittitle")[0]


def get_random_sample():
	ead_dict = defaultdict(list)
	data = []
	with open("wonky_unitdate_display_candidates.csv", mode="r") as f:
		reader = csv.reader(f)
		for row in reader:
		    ead, xpath, tag_content, text_only = row
            new_row = [text_only, tag_content]
            ead_dict[ead].append(new_row)

        # get random samples from each ead in the csv file
        for ead, examples in tqdm(ead_dict.items()):
            # print(len(examples))
            num_of_samples = int(math.ceil(len(examples) * .01))
            random_samples = random.sample(range(len(examples)), num_of_samples)

            for index in random_samples:
                random_data = examples[index]
                data.append(random_data)

    with open("random_sample.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == "__main__":
    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    grab_suspects(input_dir)
    fix_suspects(input_dir)
