# Mapping agents from EADs to ASpace
A script to add all agents (corpnames, persnames, and famnames) from a set of EADs to ASpace, then update all the EAD agent entries with their new ASpace id numbers.

##Requirements

* [lxml](http://lxml.de/)
* [NLTK](http://www.nltk.org/) (used in splitting corpnames)
* [tqdm](https://github.com/noamraph/tqdm)
* [nameparser](https://github.com/derek73/python-nameparser)
* [PySpace](https://github.com/walkerdb/bentley_code/blob/master/utilities/aspace_interface/pyspace.py)
* [EAD utilities](https://github.com/walkerdb/bentley_code/blob/master/utilities/utilities.py)

##Setup
Edit main.py with the hostname, repository number, username, and password for your archivesspace instance, as well as the intended input ead directory path.

##Usage
Just run main.py and watch it go! It may take a while.