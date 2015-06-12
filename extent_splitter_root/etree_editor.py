from lxml import etree
from collections import namedtuple


def main():
	pass

def delete_node(filepath, xpath):
	node = etree.parse(filepath).xpath(xpath)[0]
	if "physdesc" in node.getparent().tag:
		node = node.getparent()
		node.getparent().remove(node)
	else:
		print("wtf")


def get_c0x_parent_node(filepath, xpath):
	tree = etree.parse(filepath)
	c0x_parent_candidate = tree.xpath(xpath)[0]
	is_parent_tag = False

	while not is_parent_tag:
		if c0x_parent_candidate.tag.startswith("physdesc"):
			c0x_parent_candidate = c0x_parent_candidate.getparent()
			is_parent_tag = True
		else:
			c0x_parent_candidate = c0x_parent_candidate.getparent()

	xpath = tree.getpath(c0x_parent_candidate)
	return xpath


def write_aspace_extent_tags(filepath, c0x_parent_xpath, aspace_component_list):
	for aspace_component in aspace_component_list:
		physdesc = etree.Element("physdesc", altrender=aspace_component.portion)

		if aspace_component.type_:
			extent_type = etree.Element("extent", altrender="materialtype spaceoccupied")
			extent_type.text = aspace_component.type_
			physdesc.append(extent_type)

		if aspace_component.container_summary:
			container_summary = etree.Element("extent", altrender="carrier")
			physdesc.append(etree.Element())


if __name__ == "__main__":
	main()
