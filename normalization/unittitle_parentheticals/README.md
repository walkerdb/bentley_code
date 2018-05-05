# Extracting extents from unittitle parentheticals
Some parenthetical statements found in our unittitles are actually hidden extent statements. This script finds them and pulls them out into proper ```<physdesc>``` tags of their own.

For example this:

```xml
<unittitle>John Williams papers (3 linear feet)</unittitle>
```

becomes this:

```xml
<unittitle>John Williams papers</unittitle>
<physdesc>
    <extent>3 linear feet</extent>
</physdesc>
```

It only pulls out these statements if the parenthetical contains only a number and a word or phrase that matches anything in a list of known extent terms, and nothing else.

The script will also output a csv file listing edge cases that might need manual review called ```exceptions.csv```.

## Requirements
* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

## Usage

Change the output and input directory path variables in ```extents_in_unittitle_parens.py``` to fit your local needs, then run the script.

You can also add or remove additional extent terms by editing the ```extent_keywords``` list.
