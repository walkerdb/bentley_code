import csv
import os
import re
import math
import random
from collections import defaultdict

from lxml import etree
from tqdm import tqdm

def is_suspect(unittitle):
	unitdates = unittitle.xpath("unitdate")
	is_suspect_unittitle = False
	if len(unitdates) == 1:
		for unitdate in unitdates:
			if unitdate.tail:
				if len(re.findall(r'[\)\]\'\"]', unitdate.tail)) > 0 or len(unitdate.tail.strip()) > 5:
					is_suspect_unittitle = True
	elif len(unitdates) > 1:
		is_suspect_unittitle = True

	return is_suspect_unittitle

def grab_suspects():
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
	unitdate_tag_regex = r"\<\/?.*?\>"

	data = []
	for ead in tqdm(eads):
		tree = etree.parse(os.path.join(input_dir, ead))
		unittitles = tree.xpath("//unittitle")
		for unittitle in unittitles:
			if is_suspect(unittitle):
				text_with_tags = " ".join(etree.tostring(unittitle).split()).strip()
				text_without_tags = " ".join(re.sub(unitdate_tag_regex, "", text_with_tags).split()).strip()
				data.append([ead, tree.getpath(unittitle), text_with_tags, text_without_tags])

	with open('wonky_unitdate_display_candidates.csv', mode="wb") as f:
		writer = csv.writer(f)
		writer.writerows(data)
		print(len(data))

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
	grab_suspects()
	get_random_sample()