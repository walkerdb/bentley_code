#Empty unittitle fix
A script to find, categorize, and fix all instances of empty unittitles appearing in the Bentley EADs.

Will also output a list of unittitles it wasn't able to fix, in ```problem_files.csv```.

##Requirements
* [lxml](http://lxml.de/)
A script to find all empty unittitle instances

##Setup
Change all directory paths in ```empty_unittitle_fix.py``` to fit your local environment.

##Usage
Run Dallas' script to make a csv containing the locations of all empty unittitles, and make sure its output is placed in the same folder as the fix script. 

Run ```empty_unittitle_fix.py```