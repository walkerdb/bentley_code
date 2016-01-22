#Characterizing all tag/attribute pairs
Characterizes and counts all tag/attribute pairs present in a directory of EADs. Used in combination with the attribute normalization script to clean up non-controlled ead attribute values.

The output CSV is in the following form:


tag name | attribute name | attribute value | how many times this tag/attribute/value combination appears | percentage of all tags of this type that this attribute value appears on


##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Usage
Change the input directory in ```get_tag_attribute_counts.py``` to the path on your local system, then run the script.
