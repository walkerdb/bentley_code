import unittest
from mapping.aspace_agent_mapping import donors


class TestDonorImport(unittest.TestCase):
    def setUp(self):
        self.donors = [{"title": "",
                        "first name": "",
                        "middle name": "",
                        "last name": "",
                        "contact id": "9072",
                        "bhl dart id": "2000000",
                        "organization": "Skynet",
                        "suffix": "",
                        "note": "",
                        "status": "",
                        "donor number": "0989",
                        "donor part": "",
                        "folder status": ""},
                       {"title": "",
                        "first name": "Arnold",
                        "middle name": "",
                        "last name": "Schwarzenegger",
                        "contact id": "00002",
                        "bhl dart id": "200000000000000000000",
                        "organization": "Skynet",
                        "suffix": "",
                        "note": "",
                        "status": "",
                        "donor number": "1",
                        "donor part": "",
                        "folder status": "terminated"},
                       {"title": "Mrs.",
                        "first name": "Jane",
                        "middle name": "M.",
                        "last name": "Eyre",
                        "contact id": "9071",
                        "bhl dart id": "1999999",
                        "organization": "",
                        "suffix": "Jr.",
                        "note": "note!",
                        "status": "",
                        "donor number": "0001",
                        "donor part": "",
                        "folder status": "retired"}
                       ]

    def test_agent_extraction(self):
        people, corporations = donors.extract_agents(self.donors)

        self.assertTrue(all(dct in corporations for dct in self.donors[:2]) and len(corporations) == 2)
        self.assertTrue(all(dct in people for dct in self.donors[1:]) and len(people) == 2)

    def test_person_name_construction(self):
        person = self.donors[2]
        self.assertEquals(donors.make_person_name(person), u"Mrs. Jane M. Eyre Jr.")

    def test_corporation_name_construction(self):
        corp = self.donors[1]
        self.assertEquals(donors.make_corporation_name(corp), u'Skynet')