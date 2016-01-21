#Checking for self-nesting tags
A small script to check for cases where a given tag has another instance of that tag type as a parent. The idea was to use this to check for cases where the EAD standard does not allow this kind of self-nesting.

For example, it will flag this:

```xml
<unittitle>
    <unittitle>text</unittitle>
</unittitle>
```

but not this:

```xml
<unittitle>
    <unitdate>1991</unitdate>
</unittitle>
```

Its findings output to ```eads_with_nested_tags.csv```. Each row contains three data points: the name of the input ead file, the xpath to the offending tag, and the tag type.

##Requirements
* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)
* EAD Utilities

##Usage
Change the input_directory path in ```check_nested_tags.py``` to fit your local system, then run that script.