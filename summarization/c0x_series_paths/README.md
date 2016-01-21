#Characterizing and manipulating c0x "level" attribute paths
```series_exploration.py``` characterizes all possible bread-crumb trails c0x series paths can take (as taken from the "level" c0x tag attribute), counting instances of each trail type.

For example, this c0x trail

```xml
<c01 level="series">
    <c02 level="subseries">
        <c03 level="file">
            <c04 level="file">
                ...
            </c04>
        </c03>
    </c02>
</c01>
```

would be characterized as ```series->subseries->file->file```

---

```series_manipulation.py``` performs some automatic cleanup of level attributes based on the levels that come before and after.

For example, if the script finds the path ```series->subseries->item->file```, we can assume this was a mistake (since items are not meant to have children), and can tell the script to replace that "item" value with something like "file".

##Requirements
* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Usage

1. Edit both ```series_exploration.py``` and ```series_manipulation.py``` to ensure the input and output directory variables are configured to your own system.
2. Run ```series_exploration.py```. This will give you a csv document titled ```series_exploration.csv``` containing all unique c0x level breadcrumb trails, sorted by their total counts. We used this data to determine if we had any problem paths, and determine how to go about fixing them.
3. Run ```series_manipulation.py``` to transform all "item->file" paths into "file->file" paths. This script can be edited to instead transform any other subpath into whatever else you'd like it to be.