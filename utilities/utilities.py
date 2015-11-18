import os
import re

from lxml import etree
from tqdm import tqdm
from prettifydirectory import prettify_xml

class EAD(object):

    def __init__(self, filepath):
        self.path_to_ead = filepath
        self.filename = os.path.basename(self.path_to_ead)
        self.tree = etree.parse(self.path_to_ead)

    def prettyprint(self, output_dir):
        if not os.path.exists("tmp"):
            os.makedirs("tmp")

        with open(os.path.join("tmp", self.filename), mode="w") as f:
            f.write(etree.tostring(self.tree, xml_declaration=True, encoding="utf-8"))

        text = prettify_xml(self.filename, input_dir="tmp", output_dir=output_dir)

        with open(os.path.join(output_dir, self.filename), mode="w") as f:
            f.write(text)

class EADDir(object):
    def __init__(self, input_dir=r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'):
        self.input_dir = input_dir
        self.ead_files = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]

    def apply_function_to_dir(self, function, output_dir):
        for ead_file in tqdm(self.ead_files):
            ead = EAD(os.path.join(self.input_dir, ead_file))
            function(ead)
            ead.prettyprint(output_dir)

    def characterize_dir(self, function):
        results = []
        for ead_file in tqdm(self.ead_files):
            ead = EAD(os.path.join(self.input_dir, ead_file))
            result = function(ead)
            results.append(result)

        return results
