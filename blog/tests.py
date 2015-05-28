from extent_splitter import split_extents

# first, we'll define the original extent statement, something we might
# find in an average EAD &lt;extent&gt; tag
basic_extent_raw_text = "4 linear feet and 1 oversize volume."

# then let's define the list of objects we want to transform that into
basic_extent_target_output = ["4 linear feet", "1 oversize volume"]

# run the (currently unwritten) code to transform the input text,
# and store the result in a new variable
split_extent_text = split_extents(basic_extent_raw_text)

# test to see whether the result is exactly equal to our desired output
assert split_extent_text == basic_extent_target_output