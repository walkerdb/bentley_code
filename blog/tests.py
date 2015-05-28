from extent_splitter import split_extents



from unittest import TestCase

class TestExtentSplitter(TestCase):
    # "setUp" is a special reserved function that is used to define any
    # variables you will be using throughout the test. It runs before
    # anything else in the class.

    def setUp(self):
        self.basic_extent_raw_text = "4 linear feet and 1 oversize volume."
        self.basic_extent_target_output = ["4 linear feet", "1 oversize volume"]

        self.extent_with_commas = "3 linear ft., 1 oversize volume, and 5 motion picture reels"
        self.extent_with_commas_target_output = ["3 linear ft.", "1 oversize volume", "5 motion picture reels"]

    # Now for the tests. We will define each discrete test in its own
    # function. You want to be as specific as possible when creating test
    # names - this is really invaluable when figuring out exactly which
    # tests are failing, and what was being tested when they failed.

    # All tests need to start with "test" for the class to run properly

    def test_split_basic_two_element_extent_string(self):
        split_extent = split_extents(self.basic_extent_raw_text)

        # there are a number of built-in assert functions that test a
        # variety of conditions. We'll use assertEquals, which is the
        # equivalent of the assert statement we wrote above, just with
        # a much more semantically helpful name
        self.assertEquals(split_extent, self.basic_extent_target_output)

    def test_split_extent_with_commas(self):
        split_extent = split_extents(self.extent_with_commas)
        self.assertEquals(split_extent, self.extent_with_commas_target_output)

if __name__ == "__main__":
    unittest.main()