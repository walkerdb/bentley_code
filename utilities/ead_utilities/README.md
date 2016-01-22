#EAD utilities
A set of convenience utilities for simplifying common operations while working with EAD files and directories of EADs.

##Requirements
* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)
* prettifydirectory

##EAD
A convenience class to wrap common EAD functionality around a single python object. Creating an EAD object gives you access to the following:

1. the ead's filename
2. a manipulatable lxml etree representation of the ead file
3. easy prettyprinting to file

Basic usage:

```python
>>> ead = EAD(filepath="path/to/ead/file.xml")

>>> ead.filename
'file.xml'

>>> ead.tree
<lxml etree object>

```

We can also use the class to easily prettyprint the EAD file (using the ead_cleanup prettyprint function behind the scenes):

```python
ead.prettyprint(output_dir="path/to/output/directory")
```

##EADDir
A class to help perform common operations on entire directories of EAD files

The class has three primary functions:

1. Accessing basic data about the directory (eg a list of all ead files or the directory path)
2. Characterizing the content of the EAD files in the directory (for example counting all extent tags)
3. Writing changes to all EADs in the directory based on some criteria

###Using EADDir
####Initializing the object
Just call the class and give it an input directory:

```python
ead_dir = EADDir(input_dir="path/to/ead/dir")
```

####Getting at basic data
```python
>>> ead_dir.ead_files
['filename1.xml', 'filename2.xml', ...]

>>> ead_dir.input_dir
'path/to/ead/files'

>>> # manually iterating through all ead files in the directory
>>>
>>> for filename in ead_dir.ead_files:
        tree = etree.parse(os.path.join(ead_dir.input_dir, filename))
        ...
```

####Characterizing content
The ```.characterize_dir()``` method takes some characterization function and returns a list containing the results of that characterization across all eads.

For example, if I wanted to get a list of the locations of all unittitles in the EAD directory, I would make a function that finds them for a single file, then make the EADDir object and pass that function as an argument into ```.characterize_dir()```. The only catch is that the function you create must take an ead object (see above) as its input:

```python
# first define the function you'll be running on every ead file
def find_all_unittitles_in_ead(ead):
    unittitle_locations = []
    for unittitle in ead.tree.xpath("//unittitle"):
        unittitle_locations.append([ead.filename, ead.tree.getpath(unittitle)])
    
    # return your results
    return unittitle_locations

# create an EADDir object
ead_dir = EADDir(input_dir="path/to/ead/dir")

# run its characterize_dir function, passing in the function you made (without parentheses), 
# and record its final results in a variable
all_unittitle_locations = ead_dir.characterize_dir(function=find_all_unittitles_in_ead)

```

####Writing changes to a directory
A shortcut method to apply some kind of programmatic change to an entire directory of eads.

Like the characterize_dir() function, the first thing we do is create a function to make the changes we want to a single EAD file. That function should take an EAD object (see above) as its input:

```python
def YELLING_UNITTITLES(ead):
    for unittitle in ead.tree.xpath("//unittitle"):
        unittitle.text = unittitle.text.upper()

ead_dir = EADDir(input_dir="path/to/ead/dir")
ead_dir.apply_function_to_dir(function=YELLING_UNITTITLES, output_dir="path/to/output_directory")
```

Optionally, if we need our function to take an extra variable, it can be added as the "var1" keyword variable in the apply_function_to_dir() call:

```python
def correct_unittitle_words(ead, words_to_correct):
    original_word, new_word = words_to_correct
    for unittitle in ead.tree.xpath("//unittitle"):
        unittitle.text = unittitle.text.replace(original_word, new_word)

ead_dir = EADDir(input_dir="path/to/ead/dir")

ead_dir.apply_function_to_dir(function=correct_unittitle_words, output_dir="path/to/output_directory", var1=(" teh ", " the "))
```
