import unittest
from os import remove

from lxml import etree

from expand_container_ranges import expand_containers as e_c


class TestContainerExpansion(unittest.TestCase):
    def setUp(self):
        self.input = "tests/test_case_input.xml"
        self.input_xpath = "/ead/archdesc/dsc/c03/did/container"

        self.intended_output = etree.parse("tests/test_case_output.xml")

    def test_container_expansion(self):
        self.assertEquals(normalize(e_c(self.input, [[self.input_xpath, ""]], )), normalize(self.intended_output))


def normalize(xml):
    parser = etree.XMLParser(remove_blank_text=True)
    with open("temp.xml", mode="w") as f:
        f.write(etree.tostring(xml))
    xml = etree.parse("temp.xml", parser)
    for element in xml.iter():
        if element.text:
            element.text = element.text.strip(" \n\t")
    remove("temp.xml")
    return etree.tostring(xml)


if __name__ == "__main__":
    unittest.main()
