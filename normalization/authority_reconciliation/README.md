# Finding Library of Congress authority IDs for local terms
A script to automatically add Library of Congress authority ID links to controlaccess and origination terms in our EAD files.

Also updates a person's death date if our local term does not have one and the LoC version does.

##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
* [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
* EAD Utilities

##Usage
Just edit the input and output ead directory paths in the ```run.py``` file to your own intended directories, then run that script:

```
python run.py
```

_note_: this will likely take ~8-9 hours, almost entirely due to a required 2-second delay between web requests. May be a good idea to run the script overnight.

##Behind the scenes
The script's full internal workflow:

1. Extracts all unique ```persname```, ```geogname```, and ```corpname``` terms from a directory of EAD files (```grab_all_subjects.py```)
2. Looks up all of these terms in their relevant VIAF databases using its web API, returning the Library of Congress identifier for the first search result. (we use VIAF for these searches instead of the Library of Congress itself due to the fact that its search engine is much better). (```auth_search.py```)
3. Retrieves the authorized form of all of these terms from the LoC's Name Authority File (```auth_search.py```)
4. Intelligently compares all of these retrieved names with the original local term, to filter out false-positive matches (for example, due to quirks in VIAF's search sorting method, "Michael Jackson" matches to "Stevie Wonder"...) (```false_positive_check.py```)
5. With the false positives filtered out, the script writes changes back to our original EAD files (```write_new_lc_ids.py```)
    1. Writes the found Library of Congress authority web links to an "authfilenumber" attribute on their original EAD tags wherever that term is found
    2. If the tag is a persname, and if we do not have a deathdate but the LoC term does, we add that deathdate to our files.