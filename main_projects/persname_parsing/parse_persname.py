import os
import re
import csv
from collections import namedtuple

from nameparser import HumanName
from lxml import etree
from tqdm import tqdm

def grab_persnames(input_dir):
	eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
	persnames_dict = {}

	for ead in tqdm(eads):
		try:
			tree = etree.parse(os.path.join(input_dir, ead))
		except etree.XMLSyntaxError as e:
			print("Error in {0}: {1}".format(ead, e))
			continue

		persnames = tree.xpath("//controlaccess/persname") + tree.xpath("//origination/persname")
		for persname in persnames:
			auth = persname.attrib.get("authfilenumber", "")
			source = persname.attrib.get("source")
			attribs = [auth, source]
			name = persname.text.encode("utf-8")
			if name in persnames_dict:
				if auth and not persnames_dict[name]:
					persnames_dict[name] = attribs
			else:
				persnames_dict[name] = attribs

	with open("persnames.csv", mode="wb") as f:
		writer = csv.writer(f)
		data = sorted([[name, attrib[1], attrib[0]] for name, attrib in persnames_dict.items()])
		writer.writerows(data)


def parse_persname(persname, source, auth):
	ParsedName = namedtuple("ParsedName", ["title", "primary", "secondary", "suffix", "fuller_form", "birth_date", "death_date", "auth", "source"])
	alt_date_regex = r"(\d{4}) or \d{2}"
	date_regex = r"(\d{4})\??\-(?:ca\.)?((?:\d{4})?)\??"
	birth_letter_regex = r"b\. ?(\d{4})()"
	death_letter_regex = r"d\. ?()(\d{4})"
	circa_regex_1 = r"(\d{4}) \(ca\.\)-(\d{4})"
	birth_date = ""
	death_date = ""
	dates = []

	persname = re.sub(alt_date_regex, "\g<1>", persname)
	persname = persname.rstrip(".")

	for regex in [date_regex, birth_letter_regex, death_letter_regex, circa_regex_1]:
		dates = re.findall(regex, persname)

		if len(dates) == 1:
			persname = re.sub(regex, "", persname)
			persname = persname.replace(" ca.", "").rstrip(" ,")
			birth_date, death_date = dates[0]
			break

	name = HumanName(persname.decode("utf-8"))

	return ParsedName(
		title=name.title, primary=name.last, secondary=u"{0} {1}".format(name.first, name.middle).rstrip(),
		suffix=name.suffix, fuller_form=name.nickname, birth_date=birth_date, death_date=death_date,
		auth=auth, source=source
	)


if __name__ == "__main__":
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	grab_persnames(input_dir)
	output = []
	with open("persnames.csv") as f:
		reader = csv.reader(f)
		for persname, source, auth in tqdm(list(reader)):
			if "--" not in persname:
				n = parse_persname(persname, source, auth)
				output.append([persname, n.title.encode("utf-8"), n.primary.encode("utf-8"), n.secondary.encode("utf-8"), n.suffix.encode("utf-8"), n.fuller_form.encode("utf-8"), n.birth_date, n.death_date, n.auth, n.source])

	with open("parsed_persnames.csv", mode="wb") as f:
		headers = ["original name", "title", "primary", "secondary", "suffix", "fuller form", "birth date", "death date", "auth link", "source"]
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(output)

