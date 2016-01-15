import os
import csv
from copy import deepcopy

from lxml import etree
from tqdm import tqdm


def expand_containers(ead_path, xpaths):
    tree = etree.parse(ead_path)
    for xpath, text in xpaths:
        tags_present = set()
        range_node = tree.xpath(xpath)[0]
        did_node = range_node.getparent()
        c0x_node = did_node.getparent()
        c0x_parent = c0x_node.getparent()
        containers = c0x_node.xpath("did/container")

        # if there are two containers, only continue if the first is a drawer
        if len(containers) == 2:
            static_container, ranged_container = containers
            if "drawer" not in static_container.attrib["label"].lower():
                continue

        # characterize node
        for node in list(did_node) + list(c0x_node):
            tags_present.add(node.tag)

        # do flat version if node only has bare minimum of tags
        if len(tags_present) <= 3:
            base_node = deepcopy(c0x_node)
            insert_index = c0x_parent.getchildren().index(c0x_node)
            c0x_parent.remove(c0x_node)

            new_children = create_child_nodes(base_node, nested=False)

            for child in new_children:
                c0x_parent.insert(insert_index, child)
                insert_index += 1

        # do nested version if there are additional tags to account for
        else:
            if "c03" in tags_present or "c04" in tags_present:
                continue

            base_node = deepcopy(c0x_node)
            new_children = create_child_nodes(base_node)

            base_node = deepcopy(c0x_node)
            new_parent = create_parent_node(base_node)

            insert_index = c0x_parent.getchildren().index(c0x_node)
            for child in new_children:
                new_parent.append(child)

            c0x_parent.remove(c0x_node)
            c0x_parent.insert(insert_index, new_parent)

    return tree


def create_parent_node(base_node):
    for container in base_node.xpath("//did/container"):
        container.getparent().remove(container)
    return base_node


def create_child_nodes(base_node, nested=True):
    new_children = []
    c0x_parent_level = int(base_node.tag[-1])
    unittitle = base_node.xpath("did/unittitle")[0]
    containers = base_node.xpath("did/container")
    static_container = ""

    if len(containers) == 0:
        print("wtf")
        exit()
    elif len(containers) == 1:
        range_container = containers[0]
    else:
        range_container = containers[1]
        static_container = containers[0]

    start_num, endnum = map(int, range_container.text.split("-"))

    for i in range(start_num, endnum + 1):
        if nested:
            new_child_element = etree.Element("c0{0}".format(c0x_parent_level + 1), level="file")
        else:
            new_child_element = etree.Element("c0{0}".format(c0x_parent_level), level="file")
        did = etree.Element("did")
        did.append(deepcopy(unittitle))
        if type(static_container) == etree._Element:
            did.append(deepcopy(static_container))

        new_range = deepcopy(range_container)
        new_range.text = str(i)

        did.append(new_range)
        new_child_element.append(did)

        if i != start_num:
            odd = etree.Element("odd")
            odd_text = etree.Element("p")
            odd_text.text = "(continued)"
            odd.append(odd_text)
            new_child_element.append(odd)

        new_children.append(new_child_element)

    return new_children


def load_data(input_filepath):
    data_dict = {}
    with open(input_filepath, mode="r") as f:
        reader = csv.reader(f)
        for ead, ead_title, xpath, unittitle, text in reader:
            data_dict[ead] = data_dict.get(ead, [])
            data_dict[ead].append([xpath, text])
    return data_dict


if __name__ == '__main__':
    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    output_dir = "output"
    data_dict = load_data("container_ranges.csv")

    for ead, xpaths in tqdm(data_dict.items()):
        ead_path = os.path.join(input_dir, ead)
        new_tree = expand_containers(ead_path, xpaths)
        with open(os.path.join(output_dir, ead), mode="w") as f:
            f.write(etree.tostring(new_tree, pretty_print=True))
