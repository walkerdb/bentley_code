import os

from lxml import etree
from tqdm import tqdm


def normalize_attributes(input_dir, output_dir, target_tag, attribute, wrong_value_list, normal_value, remove=False):
	eads = [ead for ead in os.listdir(input_dir) if ead.endswith('.xml')]

	for ead in tqdm(eads):
		tree = etree.parse(os.path.join(input_dir, ead))
		tags = tree.xpath("//{0}".format(target_tag))

		if target_tag == "physloc" and attribute == "label":
			for tag in tags:
				if any(tag.text.lower() == text for text in ["online", "server"]):
					if tag.attrib.get(attribute, ""):
						del tag.attrib[attribute]

			with open(os.path.join(output_dir, ead), mode="w") as f:
				f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))

			continue

		for tag in tags:
			if len(wrong_value_list) > 0:
				if any([tag.attrib.get(attribute, "") == wrong_value for wrong_value in wrong_value_list]):
					if remove:
						del tag.attrib[attribute]
					else:
						tag.attrib[attribute] = normal_value
			elif remove:
				if tag.attrib.get(attribute, ""):
					del tag.attrib[attribute]
			else:
				tag.attrib[attribute] = normal_value

		with open(os.path.join(output_dir, ead), mode="w") as f:
			f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))


if __name__ == "__main__":
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	output_dir = "output"

	target_tag = "unitid"
	attribute = "repositorycode"
	wrong_value_list = ["miu-h"]
	normal_value = "MiU-H"
	remove = False

	normalize_attributes(input_dir, input_dir, target_tag, attribute, wrong_value_list, normal_value, remove)
