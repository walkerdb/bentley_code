from lxml import etree

class EAD (object):

    def __init__(self):
        self.path_to_ead = ""
        self.tree = ""

    def set_path(self, ead_path):
        self.path_to_ead = ead_path

    def make_tree(self):
        self.tree = etree.parse(self.path_to_ead)
