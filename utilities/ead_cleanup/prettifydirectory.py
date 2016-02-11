import re
import os
from os.path import join

from lxml import etree
from tqdm import tqdm


def main():
    input_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    output_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    prettify_xml_in_directory(input_directory, output_directory)


def prettify_xml_in_directory(input_dir, output_dir, eads=()):
    if not eads:
        eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]

    for filename in tqdm(eads, desc="Prettify progress", leave=True):
        text = prettify_xml(filename, input_dir, output_dir)

        # writing to file
        with open(join(output_dir, filename), mode="w") as f:
            f.write(text)


def prettify_xml(filename, input_dir, output_dir):
    parser = etree.XMLParser(remove_blank_text=True)

    tree = etree.parse(os.path.join(input_dir, filename), parser=parser)

    # prettyprint
    with open(join(output_dir, filename), mode='w') as f:
        f.write(get_string(tree))

    # re-iterate with the whitespace fix
    tree = etree.parse(join(output_dir, filename))
    fixed_text = fix_prettyprint_whitespace(get_string(tree))

    return fixed_text


def get_string(tree):
    return etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8")


def fix_prettyprint_whitespace(raw_text):
    # ensure we aren't removing essential spaces between tags
    # eg. that <tag>text <tag2>text</tag2></tag> isn't becoming <tag>text<tag2>text</tag2></tag1>
    # (the difference being one renders as "text text" and the other as "texttext")

    open_to_close_tag_regex = r'(\<\/.*?\>)(\<[^\/]*?\>)'
    item_regex = r'(\<\/item\>)\ (\<item\>)'

    text = re.sub(open_to_close_tag_regex, r'\g<1> \g<2>', raw_text)
    text = re.sub(item_regex, r'\g<1>\g<2>', text)

    return text


if __name__ == "__main__":
    main()
