import os
from os.path import join

from lxml import etree
from tqdm import tqdm


def prettify_xml_in_directory(input_dir, output_dir):
    # parser = etree.XMLParser(remove_blank_text=True)
    for filename in tqdm(os.listdir(input_dir), desc="Prettify progress", leave=True):
        if filename.endswith(".xml"):
            xml = etree.parse(join(input_dir, filename))
            with open(join(output_dir, filename), mode='w') as f:
                f.write(etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))


if __name__ == "__main__":
    input_directory = r'C:\Users\wboyle\PycharmProjects\bentley_code\one-off scripts\prettyprint_whitespace_fix\output'
    output_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    prettify_xml_in_directory(input_directory, output_directory)
