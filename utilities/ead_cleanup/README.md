#EAD prettification
Scripts to prettify our EAD files, ensuring consistent and correct indentation and spacing

##Requirements
* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Usage
To prettify all eads in a directory, use ```prettifydirectory.prettify_xml_in_directory()```. It takes an input directory, an output directory, and optionally a list of specific EADs to work on in the input directory. Without the latter it applies instead to every ead file it finds.

To prettify just one ead use ```prettifydirectory.prettify_xml()```, which takes a filename, an input directory, and an output directory.

Just simply running the script by itself will start a prettify_xml_in_directory() job - change the input and output directory variables at the bottom of the script to have this run on the paths of your choosing.

There is also a script specifically to clean up EADs spit out by the Bentley's word macro: the ```remove_newlines_and_double_spaces.py``` file. To use it, first edit its "eads" variable to contain the names of all eads to which you want it to apply, change the input and output directories to fit your local paths, then run the script. After this is run, you should re-run the main prettify script.
