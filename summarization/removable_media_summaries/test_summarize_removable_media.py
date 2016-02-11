import unittest
from lxml import etree
import summarize_removable_media as srm


class TestSummarizeRemovableMedia(unittest.TestCase):
    def setUp(self):
        self.upstream_search_tree = etree.parse("test_files/test_search_upstream.xml")
        self.upstream_search_physdescs = self.upstream_search_tree.xpath("//physdesc")
        self.digitized_material_tree = etree.parse("test_files/test_digitized_material.xml")
        self.digitized_material_physdescs = self.digitized_material_tree.xpath("//physdesc")
        self.container_tree = etree.parse("test_files/test_container_text_creation.xml")
        self.container_physdescs = self.container_tree.xpath("//physdesc")
        self.digital_object_discovery_tree = etree.parse("test_files/test_digital_object_sibling_discovery.xml")
        self.digital_object_discovery_physfacets = self.digital_object_discovery_tree.xpath("//physdesc")

    def test_extract_text(self):
        tag = etree.fromstring("""<unittitle><genreform normal="Photographs">Photographs</genreform></unittitle>""")
        text = srm.extract_text(tag)

        self.assertEquals(text, "Photographs")

    def test_container_text_creation_with_two_containers(self):
        physdesc = self.container_physdescs[0]
        containers = srm.get_containers(physdesc)
        container_text = srm.create_container_text(containers)
        self.assertEquals(container_text, "box 1, folder 2")

    def test_container_text_creation_with_no_containers(self):
        physdesc = self.container_physdescs[1]
        containers = srm.get_containers(physdesc)
        container_text = srm.create_container_text(containers)
        self.assertEquals(container_text, "[container not listed]")

    def testLocationDiscovery(self):
        self.assertEquals(srm.get_location("87207", [("box", "21")]), "Y-624-K")

    # finds digitized material
    def test_use_copies_marked_as_digitized_material(self):
        physdesc = self.digitized_material_physdescs[0]
        self.assertEquals(srm.is_digitized(physdesc), True)

    def test_digitized_marked_as_digitized_material(self):
        physdesc = self.digitized_material_physdescs[1]
        self.assertEquals(srm.is_digitized(physdesc), True)

    def test_marked_as_digitized_material_with_physfacet_keywords(self):
        physdesc = self.digitized_material_physdescs[3]
        self.assertEquals(srm.is_digitized(physdesc), True)

    def test_is_digitized_returns_false_when_not_digitized(self):
        physdesc = self.digitized_material_physdescs[2]
        self.assertEquals(srm.is_digitized(physdesc), False)

    # date search
    def test_date_found_when_there_is_an_immediate_unitdate_sibling(self):
        physdesc = self.upstream_search_physdescs[0]
        self.assertEquals(srm.get_possible_material_date(physdesc), "2017")

    def test_date_searches_upstream_when_no_immediate_unitdate_sibling(self):
        physdesc = self.upstream_search_physdescs[1]
        self.assertEquals(srm.get_possible_material_date(physdesc), "2016")

    def test_date_defaults_to_eadwide_date_when_nothing_else_is_found(self):
        physdesc = self.upstream_search_physdescs[2]
        self.assertEquals(srm.get_possible_material_date(physdesc), "2016-2017")

    # container search
    def test_container_found_when_immediate_sibling(self):
        physdesc = self.upstream_search_physdescs[0]
        self.assertEquals(srm.get_containers(physdesc), [("box", "3")])

    def test_container_found_when_no_immediate_sibling(self):
        physdesc = self.upstream_search_physdescs[1]
        self.assertEquals(srm.get_containers(physdesc), [("box", "2")])

    def test_container_defaults_to_empty_list_when_nothing_found(self):
        physdesc = self.upstream_search_physdescs[2]
        self.assertEquals(srm.get_containers(physdesc), [])

    # accessrestrict search
    def test_accessrestrict_found_when_in_same_c0x(self):
        physdesc = self.upstream_search_physdescs[0]
        self.assertEquals(srm.get_restriction(physdesc), ("ACCESS RESTRICTION 2015", "2015"))

    def test_accessrestrict_found_when_in_parent_c0x(self):
        physdesc = self.upstream_search_physdescs[1]
        self.assertEquals(srm.get_restriction(physdesc), ("ACCESS RESTRICTION 2014", "2014"))

    # digital object sibling
    def test_digital_object_discovery_with_flv_unittitle_keyword(self):
        physdesc = self.digital_object_discovery_physfacets[0]
        self.assertEquals(srm.get_digital_object_siblings(physdesc), 'filename.flv')

    def test_digital_object_discovery_with_streaming_unittitle_keyword(self):
        physdesc = self.digital_object_discovery_physfacets[1]
        self.assertEquals(srm.get_digital_object_siblings(physdesc), 'Streaming File: 85701-1')

    def test_digital_object_discovery_with_physfacet_keyword(self):
        physdesc = self.digital_object_discovery_physfacets[2]
        self.assertEquals(srm.get_digital_object_siblings(physdesc), 'Streaming File (85710-1.flv)')

    def test_digital_object_discovery_no_match_doesnt_return_anything(self):
        physdesc = self.digital_object_discovery_physfacets[3]
        self.assertEquals(srm.get_digital_object_siblings(physdesc), '')