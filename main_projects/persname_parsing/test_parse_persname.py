# coding=utf-8
import unittest
from collections import namedtuple

from parse_persname import parse_persname as parse

class TestParsePersname(unittest.TestCase):
	def setUp(self):
		self.ParsedName = namedtuple("ParsedName", ["title", "primary", "secondary", "suffix", "fuller_form", "birth_date", "death_date", "auth", "source"])

	def check_equality(self, output_data, title=u"", primary=u"", secondary=u"", suffix=u"", fuller_form=u"", birth_date="", death_date="", auth="", source=""):
		target_data = self.ParsedName(title=title, primary=primary, secondary=secondary, suffix=suffix, fuller_form=fuller_form, birth_date=birth_date, death_date=death_date, auth=auth, source=source)
		self.assertEquals(output_data, target_data)

	def test_generic_name_split(self):
		parsed_name = parse("Mott, Frank Luther, 1886-1964.", "lcnaf", "")
		self.check_equality(parsed_name, primary=u"Mott", secondary=u"Frank Luther", birth_date="1886", death_date="1964", source="lcnaf")

	def test_fullname_split(self):
		parsed_name = parse("Muller, H. J. (Hermann Joseph), 1890-1967.", "", "")
		self.check_equality(parsed_name, primary=u"Muller", secondary=u"H. J.", fuller_form=u"Hermann Joseph", birth_date="1890", death_date="1967")

	def test_special_characters(self):
		parsed_name = parse("Qāsim, Abd al-Karīm, 1914-1963", "", "")
		self.check_equality(parsed_name, primary=u"Qāsim", secondary=u"Abd al-Karīm", birth_date="1914", death_date="1963")

	def test_st(self):
		parsed_name = parse("St. Marie, Buffy.", "", "")
		self.check_equality(parsed_name, primary=u"St. Marie", secondary=u"Buffy")

	def test_birth_date(self):
		parsed_name = parse("Bonner, Campbell, b. 1876.", "", "")
		self.check_equality(parsed_name, primary=u"Bonner", secondary=u"Campbell", birth_date="1876")

	def test_death_date(self):
		parsed_name = parse("Bonner, Campbell, d. 1876.", "", "")
		self.check_equality(parsed_name, primary=u"Bonner", secondary=u"Campbell", death_date="1876")

	def test_circa_date_1(self):
		parsed_name = parse("Brady, Mathew B., 1823 (ca.)-1896.", "", "")
		self.check_equality(parsed_name, primary=u"Brady", secondary=u"Mathew B.", birth_date="1823", death_date="1896")

	def test_circa_date_2(self):
		parsed_name = parse("Brady, Mathew B., ca. 1823-", "", "")
		self.check_equality(parsed_name, primary=u"Brady", secondary=u"Mathew B.", birth_date="1823")

	def test_circa_date_3(self):
		parsed_name = parse("Chaminade, Cecile, 1857?-1944?.", "", "")
		self.check_equality(parsed_name, primary=u"Chaminade", secondary=u"Cecile", birth_date="1857", death_date="1944")

	def test_vague_date(self):
		parsed_name = parse("Cannon, Levi H., b. 1830 or 31.", "", "")
		self.check_equality(parsed_name, primary=u"Cannon", secondary=u"Levi H.", birth_date="1830")

	def test_title_placement_1(self):
		parsed_name = parse("Ballinger, Robert, Sir", "", "")
		self.check_equality(parsed_name, primary=u"Ballinger", secondary=u"Robert", title=u"Sir")

	def test_title_placement_2(self):
		parsed_name = parse("Ballinger, Robert, Mrs.", "", "")
		self.check_equality(parsed_name, primary=u"Ballinger", secondary=u"Robert", title=u"Mrs.")

	def test_name_with_subject(self):
		parsed_name = parse("Hubbard, Bela, 1814-1896--Michigan maps--Vol.8", "", "")
		self.check_equality(parsed_name, primary=u"Hubbard", secondary=u"Bela", birth_date="1814", death_date="1896")

	def test_royal_in_name(self):
		parsed_name = parse("Copeland, Royal S", "", "")
		self.check_equality(parsed_name, primary=u"Copeland", secondary=u"Royal S", title=u"")

	def test_queen_of_england(self):
		parsed_name = parse("Elizabeth II, Queen of Great Britain, 1926-", "", "")
		self.check_equality(parsed_name, primary=u"Elizabeth", suffix=u"II", title=u"Queen of Great Britain", birth_date="1926", secondary=u"")

	def test_dalai_lama(self):
		parsed_name = parse("Bstan-Ädzin-rgya-mtsho, Dalai Lama XIV, 1935-", "", "")
		self.check_equality(parsed_name, primary=u"Bstan-Ädzin-rgya-mtsho", title=u"Dalai Lama XIV", birth_date="1935")


if __name__ == "__main__":
	unittest.main()