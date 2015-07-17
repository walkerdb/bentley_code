import unittest

from fix_whitespace_lost_in_prettyprint import fix_prettyprint_whitespace as fix

class TestLostWhitespaceFix(unittest.TestCase):

	def test_base_case(self):
		self.assertEquals(fix("</tagone><tagtwo>"), "</tagone> <tagtwo>")

	def test_unchanged(self):
		self.assertEquals(fix("<tagone><tagtwo>"), "<tagone><tagtwo>")

	def test_complicated(self):
		self.assertEquals(fix("some text</a><a>more text"), "some text</a> <a>more text")

	def test_item(self):
		self.assertEquals(fix("</item><item>"), "</item><item>")

	def test_item2(self):
		self.assertEquals(fix("""</title></item><item><title render="italic">"""), """</title></item><item><title render="italic">""")

if __name__ == "__main__":
	unittest.main()