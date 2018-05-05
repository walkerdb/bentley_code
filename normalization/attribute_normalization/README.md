# Tool for changing attribute values globally
A general utility script that searches through all matching tag/attribute pairs and normalizes those attribute values to some other given value.

## Requirements
* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

## Usage
The following variables (found at the bottom of the script) should be edited to your needs:

* ```input_dir```: the source EAD directory
* ```output_dir```: where to output the changed EAD files
* ```target_tag```: name of the tag that contains the attribute you want to normalize
* ```attribute```: name of the attribute that you are targeting
* ```wrong_value_list```: a list of all incorrect values that will be changed to one single correct value
* ```normal_value```: what to change all the incorrect values into (needs to be a string)
* ```remove```: If true, the script will instead remove the attribute entirely if it has an incorrect value. False by default.
