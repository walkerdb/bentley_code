# coding=utf-8
import unittest

from parse_persname import parse_persname as parse


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
        for key in self.keys:
            if key not in dct:
                dct[key] = u""

        self.assertEquals(output_data, dct)

    def test_generic_name_split(self):
        parsed_name = parse("Mott, Frank Luther, 1886-1964.", "lcnaf", "")
        self.check_equality(parsed_name, {u"primary_name": u"Mott", u"rest_of_name": u"Frank Luther", u"birth_date": u"1886", u"death_date": u"1964", u"date_string": u"1886-1964", u"source": u"lcnaf"})

    def test_fullname_split(self):
        parsed_name = parse("Muller, H. J. (Hermann Joseph), 1890-1967.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Muller", u"rest_of_name": u"H. J.", u"fuller_form": u"Hermann Joseph", u"birth_date": u"1890", u"death_date": u"1967", u"date_string": u"1890-1967"})

    def test_special_characters(self):
        parsed_name = parse("Qāsim, Abd al-Karīm, 1914-1963", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Qāsim", u"rest_of_name": u"Abd al-Karīm", u"birth_date": u"1914", u"death_date": u"1963", u"date_string": u"1914-1963"})

    def test_st(self):
        parsed_name = parse("St. Marie, Buffy.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"St. Marie", u"rest_of_name": u"Buffy"})

    def test_birth_date(self):
        parsed_name = parse("Bonner, Campbell, b. 1876.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Bonner", u"rest_of_name": u"Campbell", u"birth_date": u"1876", u"date_string": u"b. 1876"})

    def test_death_date(self):
        parsed_name = parse("Bonner, Campbell, d. 1876.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Bonner", u"rest_of_name": u"Campbell", u"death_date": u"1876", u"date_string": u"d. 1876"})

    def test_circa_date_1(self):
        parsed_name = parse("Brady, Mathew B., 1823 (ca.)-1896.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Brady", u"rest_of_name": u"Mathew B.", u"birth_date": u"1823", u"death_date": u"1896", u"date_string": u"1823-1896"})

    def test_circa_date_2(self):
        parsed_name = parse("Brady, Mathew B., ca. 1823-", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Brady", u"rest_of_name": u"Mathew B.", u"birth_date": u"1823", u"date_string": u"b. 1823"})

    def test_circa_date_3(self):
        parsed_name = parse("Chaminade, Cecile, 1857?-1944?.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Chaminade", u"rest_of_name": u"Cecile", u"birth_date": u"1857", u"death_date": u"1944", u"date_string": u"1857-1944"})

    def test_vague_date(self):
        parsed_name = parse("Cannon, Levi H., b. 1830 or 31.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Cannon", u"rest_of_name": u"Levi H.", u"birth_date": u"1830", u"date_string": u"b. 1830"})

    def test_title_placement_1(self):
        parsed_name = parse("Ballinger, Robert, Sir", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Ballinger", u"rest_of_name": u"Robert", u"title": u"Sir"})

    def test_title_placement_2(self):
        parsed_name = parse("Ballinger, Robert, Mrs.", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Ballinger", u"rest_of_name": u"Robert", u"title": u"Mrs."})

    def test_name_with_subject(self):
        parsed_name = parse("Hubbard, Bela, 1814-1896--Michigan maps--Vol.8", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Hubbard", u"rest_of_name": u"Bela", u"birth_date": u"1814", u"death_date": u"1896", u"date_string": u"1814-1896"})

    def test_royal_in_name(self):
        parsed_name = parse("Copeland, Royal S", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Copeland", u"rest_of_name": u"Royal S", u"title": u""})

    def test_queen_of_england(self):
        parsed_name = parse("Elizabeth II, Queen of Great Britain, 1926-", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Elizabeth", u"numbers": u"II", u"title": u"Queen of Great Britain", u"birth_date": u"1926", u"rest_of_name": u"", u"date_string": u"b. 1926"})

    def test_dalai_lama(self):
        parsed_name = parse("Bstan-Ädzin-rgya-mtsho, Dalai Lama XIV, 1935-", "", "")
        self.check_equality(parsed_name, {u"primary_name": u"Bstan-Ädzin-rgya-mtsho", u"title": u"Dalai Lama XIV", u"birth_date": u"1935", u"date_string": u"b. 1935"})


if __name__ == "__main__":
    unittest.main()
