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
			action = determine_action(unittitle)
			if action:
				text_with_tags = " ".join(etree.tostring(unittitle).split()).strip()
				text_without_tags = " ".join(re.sub(tag_regex, "", text_with_tags).split()).strip()
				data.append([ead, tree.getpath(unittitle), text_with_tags, text_without_tags, action])

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
		for filename, xpath, text_with_tags, text_without_tags, action in tqdm(items):
			example_dict[filename] = example_dict.get(filename, [])
			example_dict[filename].append((xpath, action))

		for ead, dict_value_list in tqdm(example_dict.items()):
			tree = etree.parse(os.path.join(input_dir, ead))

			for xpath, action in dict_value_list:
				unittitle = tree.xpath(xpath)[0]
				move_unitdates(unittitle, action)

			with open(os.path.join("output", ead), mode="w") as f:
				f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))


def determine_action(unittitle):
	unitdates = unittitle.xpath("unitdate")
	action = ""
	if len(unitdates) >= 1:
		for unitdate in unitdates:
			if unitdate.tail:
				if len(unitdate.tail.strip(", 1234567890-")) > 5 and len(unitdates) > 1:
					action = "move_and_calcify"
				elif any([unitdate.tail.strip() == candidate for candidate in [",", "and", ", and"]]):
					tails = [unitdate.tail if unitdate.tail else "" for unitdate in unitdates]
					print(tails)
					if all([len(tail.strip(" and,.")) == 0 for tail in tails]):
						action = "move_and_clean"

	return action


def move_unitdates(unittitle_node, action):
	parent = unittitle_node.getparent()
	unitdates = unittitle_node.xpath("unitdate")

	tag_regex = r"<unitdate.*?>(.*?)<\/unitdate>"

	copies = []
	for unitdate in unitdates:
		copies.append(deepcopy(unitdate))

	if action == "move_and_calcify":
		new_unittitle = etree.fromstring(re.sub(tag_regex, '\g<1>', etree.tostring(unittitle_node)))

	else:
		new_unittitle = etree.fromstring(re.sub(tag_regex, '', etree.tostring(unittitle_node)))
		new_unittitle.text = new_unittitle.text.strip(" ,")
		if new_unittitle.text.endswith("and"):
			new_unittitle.text = new_unittitle.text[:-4]
			new_unittitle.text = new_unittitle.text.strip(" ,")

	parent.insert(parent.index(unittitle_node), new_unittitle)
	parent.remove(unittitle_node)

	for i, copy in enumerate(copies):
		copy.tail = ""
		parent.insert(parent.index(new_unittitle) + 1 + i, copy)  # adding i to ensure original order is preserved
	print(etree.tostring(parent))

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
	# fix_suspects(input_dir)