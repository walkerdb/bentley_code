from lxml import etree
from collections import namedtuple


def main():
	pass

def delete_node(tree, xpath):
	node = tree.xpath(xpath)[0]
	# print(etree.tostring(node.getparent(), pretty_print=True))
	if "physdesc" in node.getparent().tag:
		node = node.getparent()
		parent = node.getparent()
		parent.remove(node)
	else:
		print("wtf")

	# print(etree.tostring(node, pretty_print=True))

	return tree


def get_parent_node(tree, xpath):
	try:
		c0x_parent_candidate = tree.xpath(xpath)[0]
	except:
		print("whaa? {0}".format(xpath))

	is_parent_tag = False

	while not is_parent_tag:
		if c0x_parent_candidate.tag.startswith("physdesc"):
			c0x_parent_candidate = c0x_parent_candidate.getparent()
			is_parent_tag = True
		else:
			c0x_parent_candidate = c0x_parent_candidate.getparent()

	xpath = tree.getpath(c0x_parent_candidate)
	return xpath


def write_aspace_extent_tags(filename, tree, target_xpath, aspace_components):
	target_node = tree.xpath(target_xpath)[0]

	for aspace_component in aspace_components:
		physdesc = etree.Element("physdesc", altrender=aspace_component.portion)

		if aspace_component.type_:
			extent_type = build_etree_element(tag="extent", altrender="materialtype spaceoccupied", text=aspace_component.type_)
			physdesc.append(extent_type)

		if aspace_component.container_summary:
			container_summary = build_etree_element(tag="extent", altrender="carrier", text=aspace_component.container_summary)
			physdesc.append(container_summary)

		if aspace_component.physfacet:
			physfacet = build_etree_element(tag="physfacet", text=aspace_component.physfacet)
			physdesc.append(physfacet)

		if aspace_component.dimensions:
			dimensions = build_etree_element(tag="dimensions", text=aspace_component.dimensions)
			physdesc.append(dimensions)

		target_node.insert(1, physdesc)

		# if len(list(physdesc)) > 1:
		# 	print(etree.tostring(physdesc, pretty_print=True))

	return tree

def build_etree_element(tag, text, altrender=""):
	element = etree.Element(tag, altrender=altrender) if altrender else etree.Element(tag)
	element.text = text
	return element


if __name__ == "__main__":
	main()
