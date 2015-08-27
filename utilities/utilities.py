import os
import re

from lxml import etree

class EAD (object):

    def __init__(self, filepath):
        self.path_to_ead = filepath
        self.filename = os.path.basename(self.path_to_ead)
        self.tree = etree.parse(self.path_to_ead)

    def prettyprint(self, output_dir):
        with open(os.path.join(output_dir, self.filename), mode="w") as f:
            fixed_text = self.__fix_prettyprint_whitespace__(
                etree.tostring(self.tree, pretty_print=True, xml_declaration=True, encoding="utf-8")
            )
            f.write(fixed_text)

    @staticmethod
    def __fix_prettyprint_whitespace__(raw_text):
        open_to_close_tag_regex = r'(\<\/.*?\>)(\<[^\/]*?\>)'
        item_regex = r'(\<\/item\>)\ (\<item\>)'

        text = re.sub(open_to_close_tag_regex, r'\g<1> \g<2>', raw_text)
        text = re.sub(item_regex, r'\g<1>\g<2>', text)

        return text
