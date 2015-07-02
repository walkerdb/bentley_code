import unittest
from os import remove

from lxml.etree import parse, tostring, XMLParser

from main_projects.empty_unittitle_fix import empty_unittitle_fix as euf

parser = XMLParser(remove_blank_text=True)

class TestResults(unittest.TestCase):
    def setUp(self):
        # loads all the data the program needs for the tests

        directory = 'S:/Curation/Student Work/Walker Boyle/Test environment/empty_unittitle_fix/examples/'
        # file locations
        self.loc_perfect = [directory + "perfect.xml", "/ead/archdesc/dsc/c04[1]"]
        self.loc_empty = [directory + "empty.xml", "/ead/archdesc/dsc/c04[1]"]
        self.loc_box_unchanged = [directory + "box_only_unchanged.xml", "/ead/archdesc/dsc/c04[2]"]
        self.loc_box_changed = [directory + "box_only_changed.xml", "/ead/archdesc/dsc/c04[2]"]
        self.loc_mult_containers_unchanged = [directory + "multiple_containers_unchanged.xml", "/ead/archdesc/dsc/c04[2]"]
        self.loc_odd_to_parent_node = [directory + "odd_to_parent_node.xml", "/ead/archdesc/dsc/c02/c03"]
        self.loc_extent_to_parent_node = [directory + "extent_to_parent_node.xml", "/ead/archdesc/dsc/c02/c03"]

        # lxml objects
        self.lxml_perfect = parse("examples/perfect.xml")
        self.lxml_empty_corrected = parse("examples/empty_corrected.xml")
        self.lxml_box_unchanged_corrected = parse("examples/box_only_unchanged_corrected.xml")
        self.lxml_box_changed = parse("examples/box_only_changed.xml")
        self.lxml_mult_containers_unchanged_corrected = parse("examples/multiple_containers_unchanged_corrected.xml")
        self.lxml_upper_neighbor = parse("examples/test_upper_neighbor.xml")
        self.lxml_odd_to_parent_node_corrected = parse("examples/odd_to_parent_node_corrected.xml")
        self.lxml_extent_to_parent_node_corrected = parse("examples/extent_to_parent_node_corrected.xml")

        # reset output file
        output = open("output/problem_files.csv", mode="w")
        output.close()

        with open("examples/problem_file_output.csv", mode = "r") as f:
            self.problem_file_output = f.read()



    # find_upper_neighbor code works properly on siblings and parents
    def test_find_upper_neighbor_method_sibling(self):
        original_xpath = "/ead/archdesc/dsc/c03/c04[3]/did/container"
        sib_xpath = "/ead/archdesc/dsc/c03/c04[2]"
        processed_xpath = euf.retrieve_upper_c0x_neighbor_xpath(self.lxml_upper_neighbor, original_xpath)
        self.assertEqual(processed_xpath, sib_xpath)

    def test_find_upper_neighbor_method_parent(self):
        original_xpath = "/ead/archdesc/dsc/c03/did"
        parent_xpath = "/ead/archdesc/dsc/c03"
        processed_xpath = euf.retrieve_upper_c0x_neighbor_xpath(self.lxml_upper_neighbor, original_xpath)
        self.assertEqual(processed_xpath, parent_xpath)

    # don't do anything to proper xml
    def test_no_false_positives(self):
        processed = euf.process_file(self.loc_perfect[0], self.loc_perfect[1])
        self.assertEqual(normalize(processed), normalize(self.lxml_perfect))

    # If the whole thing is completely blank, delete it.
    def test_delete_blank_node(self):
        processed = euf.process_file(self.loc_empty[0], self.loc_empty[1])
        self.assertEqual(normalize(processed), normalize(self.lxml_empty_corrected))

    # If all but the box number is completely blank delete it
    def test_multiple_boxes_one_box_number(self):
        processed = euf.process_file(self.loc_box_unchanged[0], self.loc_box_unchanged[1])
        self.assertEqual(normalize(processed), normalize(self.lxml_box_unchanged_corrected))

    # but only if the container number is the same as what precedes it
    def test_multiple_containers_different_numbers(self):
        processed = euf.process_file(self.loc_box_changed[0], self.loc_box_changed[1])
        self.assertEqual(processed, "")

    def test_multiple_containers_unchanged_still_deletes(self):
        processed = euf.process_file(self.loc_mult_containers_unchanged[0], self.loc_mult_containers_unchanged[1])
        self.assertEqual(normalize(processed), normalize(self.lxml_mult_containers_unchanged_corrected))

    # containers change, write filename and xpath to file, leave unchanged
    def test_failures_write_to_file(self):
        euf.process_file(self.loc_box_changed[0], self.loc_box_changed[1])
        with open("output/problem_files.csv") as f:
            data = f.read()
        self.assertEquals(data.strip("\n"), self.problem_file_output.strip("\n"))

    # If only has an <odd> tag, append <odd> to upper c0x neighbor
    def test_append_odd_and_box_number_to_upper_neighbor(self):
        processed = euf.process_file(self.loc_odd_to_parent_node[0], self.loc_odd_to_parent_node[1])
        self.assertEqual(normalize(processed), normalize(self.lxml_odd_to_parent_node_corrected))

    # If only has extents tag, append to upper c0x neighbor
    def test_extent_only_append_to_upper_neighbor(self):
        processed = euf.process_file(self.loc_extent_to_parent_node[0], self.loc_extent_to_parent_node[1])
        self.assertEqual(normalize(processed), normalize(self.lxml_extent_to_parent_node_corrected))


def normalize(xml):
    with open("temp.xml", mode="w") as f:
        f.write(tostring(xml))
    xml = parse("temp.xml", parser)
    for element in xml.iter():
        if element.text:
            element.text = element.text.strip(" \n\t")
    remove("temp.xml")
    return tostring(xml)


if __name__ == "__main__":
    unittest.main()