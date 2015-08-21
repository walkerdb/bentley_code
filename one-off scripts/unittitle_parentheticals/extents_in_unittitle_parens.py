import os
import re
import csv
from collections import defaultdict

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
				parenthetical = re.search(r'([\(\[].*?[\)\]])', text)
				parenthetical = parenthetical.group(1) if parenthetical else ""
				if parenthetical.strip("()[] 1234567890"):
					if parenthetical.strip("()[] ")[0].isdigit() \
						and not re.search(r"\d{4}|\dth|\dst|\dnd|\d,\d{3}|\-[A-Z]\)|\d[A-Z]", parenthetical) \
						and "/" not in parenthetical:

						output.append([ead, xpath, text_without_xml, parenthetical, text])
	return output


def move_extent_parens(input_dir, output_dir, input):
	keywords = ['album', 'audiotape', 'binder', 'book', 'box', 'boxes', 'cases', 'cassette', 'disc', 'disk', 'drawing',
				'envelope', 'file', 'folder', 'image', 'issue', 'item', 'linear feet', 'map', 'neg', 'negative',
				'notebook', 'photo', 'poster', 'reel', 'slide', 'tape', 'v.', 'vol.', 'volume']
	input.reverse()

	input_dict = defaultdict(list)
	for item in input:
		input_dict[item[0]].append(item[1:])

	for ead, candidate_list in input_dict.items():
		tree = etree.parse(os.path.join(input_dir, ead))

		for candidate in candidate_list:
			xpath, text_without_xml, parenthetical, text = candidate

			try:
				unittitle_node = tree.xpath(xpath)[0]
			except IndexError:
				print("Failed to grab xpath in {} -- {}".format(ead, xpath))
				continue

			# check if the parenthetical has an extent keyword
			if any([keyword in parenthetical for keyword in keywords]) and " of " not in parenthetical:

				# If there is already an extent in this c0x item, skip over this entry (there are only a few of these)
				if any([tag.tag == "extent" for tag in unittitle_node.getparent().iter()]):
					print("{} - {}\nthere's an extent already here!\n{}\n{}".format(ead, xpath, parenthetical, etree.tostring(unittitle_node.getparent().xpath("physdesc")[0])))
					continue

				# remove the parenthetical from the unittitle text (this is on a tostring'd unittitle)
				# we're using the tostring version because that is the easiest way to preserve interior tags
				text = " ".join(text.replace(parenthetical, "").strip().split()).replace(" </unittitle>", "</unittitle>")

				# create a new unittitle from this text
				new_unittitle = etree.fromstring(text)

				# remove old unittitle and add new version where the old one was
				parent = unittitle_node.getparent()
				parent.insert(parent.index(unittitle_node), new_unittitle)
				parent.remove(unittitle_node)

				# build the new extent and append it to the <did>
				extent_text = parenthetical.strip("()[] ")
				physfacet = etree.Element("physdesc")
				extent = etree.Element("extent")
				extent.text = extent_text
				physfacet.append(extent)
				parent.append(physfacet)

		with open(os.path.join(output_dir, ead), mode="w") as xml:
			xml.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))




if __name__ == "__main__":
	input_dir = r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all"
	output_dir = r"C:\Users\wboyle\PycharmProjects\bentley_code\one-off scripts\unittitle_parentheticals\output"
	candidates = find_parens(input_dir)
	move_extent_parens(input_dir, output_dir, candidates)


