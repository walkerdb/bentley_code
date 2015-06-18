from lxml import etree
import os
from os.path import join

from tqdm import tqdm


def prettify_xml_in_directory(input_dir, output_dir):
    parser = etree.XMLParser(remove_blank_text=True)
    for filename in tqdm(os.listdir(input_dir), desc="Prettify progress", leave=True):
        if filename.endswith(".xml"):
            xml = etree.parse(join(input_dir, filename), parser)
            with open(join(output_dir, filename), mode='w') as f:
                f.write(etree.tostring(xml, pretty_print=True))


if __name__ == "__main__":
    input_directory = r"C:\Users\wboyle\PycharmProjects\bentley_code\extent_splitter_root\output"
    output_directory = r"C:\Users\wboyle\PycharmProjects\bentley_code\extent_splitter_root\output"
    prettify_xml_in_directory(input_directory, output_directory)