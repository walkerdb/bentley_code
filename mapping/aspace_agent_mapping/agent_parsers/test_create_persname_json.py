# coding=utf-8
import unittest

from mapping.aspace_agent_mapping.agent_parsers import parse_persname as parse


class TestParsePersname(unittest.TestCase):
    def setUp(self):
        self.keys = [u"title",
                     u"primary_name",
                     u"rest_of_name",
                     u"suffix",
                     u"fuller_form",
                     u"numbers",
                     u"birth_date",
                     u"death_date",
                     u"date_string",
                     u"auth",
                     u"source"]

    def check_equality(self, output_data, dct):
        dct[u"sort_name_auto_generate"] = True
        dct[u"name_order"] = u"inverted"

        self.assertEquals(output_data, dct)

    def test_generic_name_split(self):
        parsed_name = parse(u"Mott, Frank Luther, 1886-1964.", u"", u"lcnaf")
        self.check_equality(parsed_name, {u"primary_name": u"Mott", u"rest_of_name": u"Frank Luther", u"birth_date": u"1886", u"death_date": u"1964", u"date_string": u"1886-1964", u"source": u"lcnaf"})

    def test_fullname_split(self):
        parsed_name = parse(u"Muller, H. J. (Hermann Joseph), 1890-1967.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Muller", u"rest_of_name": u"H. J.", u"fuller_form": u"Hermann Joseph", u"birth_date": u"1890", u"death_date": u"1967", u"date_string": u"1890-1967"})

    def test_special_characters(self):
        parsed_name = parse(u"Qāsim, Abd al-Karīm, 1914-1963", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Qāsim", u"rest_of_name": u"Abd al-Karīm", u"birth_date": u"1914", u"death_date": u"1963", u"date_string": u"1914-1963"})

    def test_st(self):
        parsed_name = parse(u"St. Marie, Buffy.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"St. Marie", u"rest_of_name": u"Buffy"})

    def test_birth_date(self):
        parsed_name = parse(u"Bonner, Campbell, b. 1876.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Bonner", u"rest_of_name": u"Campbell", u"birth_date": u"1876", u"date_string": u"b. 1876"})

    def test_death_date(self):
        parsed_name = parse(u"Bonner, Campbell, d. 1876.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Bonner", u"rest_of_name": u"Campbell", u"death_date": u"1876", u"date_string": u"d. 1876"})

    def test_circa_date_1(self):
        parsed_name = parse(u"Brady, Mathew B., 1823 (ca.)-1896.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Brady", u"rest_of_name": u"Mathew B.", u"birth_date": u"1823", u"death_date": u"1896", u"date_string": u"1823-1896"})

    def test_circa_date_2(self):
        parsed_name = parse(u"Brady, Mathew B., ca. 1823-", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Brady", u"rest_of_name": u"Mathew B.", u"birth_date": u"1823", u"date_string": u"b. 1823"})

    def test_circa_date_3(self):
        parsed_name = parse(u"Chaminade, Cecile, 1857?-1944?.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Chaminade", u"rest_of_name": u"Cecile", u"birth_date": u"1857", u"death_date": u"1944", u"date_string": u"1857-1944"})

    def test_vague_date(self):
        parsed_name = parse(u"Cannon, Levi H., b. 1830 or 31.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Cannon", u"rest_of_name": u"Levi H.", u"birth_date": u"1830", u"date_string": u"b. 1830"})

    def test_title_placement_1(self):
        parsed_name = parse(u"Ballinger, Robert, Sir", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Ballinger", u"rest_of_name": u"Robert", u"title": u"Sir"})

    def test_title_placement_2(self):
        parsed_name = parse(u"Ballinger, Robert, Mrs.", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Ballinger", u"rest_of_name": u"Robert", u"title": u"Mrs."})

    def test_name_with_subject(self):
        parsed_name = parse(u"Hubbard, Bela, 1814-1896", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Hubbard", u"rest_of_name": u"Bela", u"birth_date": u"1814", u"death_date": u"1896", u"date_string": u"1814-1896"})

    def test_royal_in_name(self):
        parsed_name = parse(u"Copeland, Royal S", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Copeland", u"rest_of_name": u"Royal S"})

    def test_queen_of_england(self):
        parsed_name = parse(u"Elizabeth II, Queen of Great Britain, 1926-", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Elizabeth", u"numbers": u"II", u"title": u"Queen of Great Britain", u"birth_date": u"1926", u"date_string": u"b. 1926"})

    def test_dalai_lama(self):
        parsed_name = parse(u"Bstan-Ädzin-rgya-mtsho, Dalai Lama XIV, 1935-", u"", u"")
        self.check_equality(parsed_name, {u"primary_name": u"Bstan-Ädzin-rgya-mtsho", u"title": u"Dalai Lama XIV", u"birth_date": u"1935", u"date_string": u"b. 1935"})


if __name__ == "__main__":
    unittest.main()
