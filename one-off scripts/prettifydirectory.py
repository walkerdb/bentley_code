import re
import os
from os.path import join
from copy import deepcopy

from lxml import etree
from tqdm import tqdm


def prettify_xml_in_directory(input_dir, output_dir):
    parser = etree.XMLParser(remove_blank_text=True)
    tags_to_leave_alone = ['arrangement', 'accessrestrict', 'bioghist', 'scopecontent', 'relatedmaterial', 'otherfindaid', 'altformavail']

    eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
    for filename in tqdm(eads, desc="Prettify progress", leave=True):
        tree = etree.parse(join(input_dir, filename))

        # first, remove the tags to leave alone
        removed_items = remove_tags(tree, tags_to_leave_alone)

        # re-read the tree with the custom parser
        with open(join(output_dir, filename), mode="w") as f:
            f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))

        new_tree = etree.parse(os.path.join(output_dir, filename), parser=parser)
        del tree

        # prettyprint
        with open(join(output_dir, filename), mode='w') as f:
            f.write(etree.tostring(new_tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))

        # re-iterate with the whitespace fix
        tree = etree.parse(join(output_dir, filename))
        fixed_text = fix_prettyprint_whitespace(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        del tree
        fixed_tree = etree.fromstring(fixed_text).getroottree()

        # finally re-add the removed tags
        add_tags(fixed_tree, removed_items)

        with open(join(output_dir, filename), mode="w") as f:
            text = etree.tostring(fixed_tree, pretty_print=True, xml_declaration=True, encoding="utf-8")
            f.write(text)



def fix_prettyprint_whitespace(raw_text):
    open_to_close_tag_regex = r'(\<\/.*?\>)(\<[^\/]*?\>)'
    item_regex = r'(\<\/item\>)\ (\<item\>)'

    text = re.sub(open_to_close_tag_regex, r'\g<1> \g<2>', raw_text)
    text = re.sub(item_regex, r'\g<1>\g<2>', text)

    return text


def remove_tags(tree, tags_to_leave_alone):
    removed_items = []
    for tag_type in tags_to_leave_alone:
        tags = tree.xpath("//{}".format(tag_type))
        tags.reverse()
        removed_items += [(tree.getpath(tag.getparent()), list(tag.getparent()).index(tag), deepcopy(tag)) for tag in tags]
        for tag in tags:
            tag.getparent().remove(tag)

    return removed_items


def add_tags(tree, tags_to_add):
    tags_to_add.reverse()
    for xpath, index, tag in tags_to_add:
        try:
            parent = tree.xpath(xpath)[0]
            parent.insert(index, tag)
        except IndexError:
            print("failed")



if __name__ == "__main__":
    input_directory = r"C:\Users\wboyle\PycharmProjects\bentley_code\one-off scripts\unitdates_in_unittitles\output"
    output_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    prettify_xml_in_directory(output_directory, output_directory)


