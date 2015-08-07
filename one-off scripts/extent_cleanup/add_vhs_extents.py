import os

from lxml import etree
from tqdm import tqdm

input_file = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all\englerj.xml'

tree = etree.parse(input_file)

vhs_c03 = tree.xpath("/ead/archdesc/dsc/c01[2]/c02[2]/c03[8]")[0]

c04s = vhs_c03.xpath("c04")

for c04 in c04s:
	did = c04.xpath("did")[0]
	physdesc = did.xpath("physdesc")
	if len(physdesc) == 1:
		extent = physdesc[0].xpath("extent")
		if len(extent) == 1:
			text = extent[0].text
			try:
				if "VHS" in text:
					continue
				else:
					extent[0].text = "1 VHS Tape ({0})".format(text)
			except TypeError:
				print(etree.tostring(c04))
	else:
		extent = etree.Element("extent")
		extent.text = "1 VHS Tape"
		physdesc = etree.Element("physdesc")
		physdesc.append(extent)
		did.append(physdesc)

with open("englerj.xml", mode="w") as f:
	f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))
