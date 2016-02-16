from lxml import etree


def delete_node(tree, xpath):
    node = tree.xpath(xpath)[0]

    # this code is specific to extents
    node = node.getparent()
    parent = node.getparent()
    parent.remove(node)

    return tree


def get_parent_node(tree, xpath):
    try:
        parent_candidate = tree.xpath(xpath)[0]
    except:
        return NotImplementedError("broken xpath -- no idea why!")

    is_parent_tag = False

    while not is_parent_tag:
        if parent_candidate.tag.startswith("physdesc"):
            parent_candidate = parent_candidate.getparent()
            is_parent_tag = True
        else:
            parent_candidate = parent_candidate.getparent()

    xpath = tree.getpath(parent_candidate)
    return xpath


def make_aspace_formatted_physdesc(aspace_components):
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

        return physdesc


def add_new_physdescs_to_tree(tree, new_physdescs):
    for xpath, physdesc_list in new_physdescs.items():
        parent_node = tree.xpath(xpath)[0]
        physdesc_list.reverse()

        current_physdescs = parent_node.xpath("physdesc")
        if not current_physdescs:
            index = parent_node.index(parent_node.xpath("unittitle")[0])
        else:
            index = parent_node.index(current_physdescs[-1])

        for physdesc in physdesc_list:
            parent_node.insert(index + 1, physdesc)


def build_etree_element(tag, text, altrender=""):
    element = etree.Element(tag, altrender=altrender) if altrender else etree.Element(tag)
    element.text = text
    return element
