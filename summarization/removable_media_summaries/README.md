#Removable media summaries
Extracts all removable digital media extents from a directory of eads and creates an inventory (with a number of added fields) and two summary files, all in csv format.

##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)
* EAD utilities

##Usage
Change the ead input directory in the main script, then run it!

There is an option to also include analog media in the summary (film, tapes, etc). To include these, set ```digital_only``` in the ```main()``` method to ```False```.


##Output
Three files are created: one overall inventory, one summary grouped by EAD, and one summary grouped by media type.

The following fields are included in the inventory:

```python
"ead name"                 # the filename of the ead
"ead id"                   # the id number for that ead file
"collection name"          # the full name of the collection the ead describes
"number of items"          # number of items encompassed in the current row
"extent type"              # the type of extent (optical disk, usb drive, etc.)
"physfacet text"           # the physfacet (CD, DVD, 3.5", etc)
"size (mb)"                # how large the raw disk-image copy of the original media would be if digitized
"location"                 # where in the stacks the item can be found. Usually a range of locations
"container"                # usually box number
"potential date of material"  # a guess at when the material may have been made. Not guaranteed to be accurate
"title of potentially related digital content (if any)"  # if there are any related digital files
"is the result of a Bentley digitization project"  # whether or not the media is from a prior digitization project
"access restrictions"      # currently-present access restrictions
"access restiction dates"  # dates associated with the above
"uuid"                     # the uuid of the c-level element the item appears in
"unittitle breadcrumb"     # a backup way to reconstruct where in the finding-aid this extent appeared. 
                           # It's a breadcrumb trail of all parent unittitles leading up to the unittitle of the element being described
```