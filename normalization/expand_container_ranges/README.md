#Expanding container ranges
This script finds all examples of c0x items that contain a container with ranges, then creates individual child c0x items for each container number described in that range, retaining all necessary context from the original entry.

For example, something like this:

```xml
<c03 level="file">
    <did>
        <container type="box" label="Drawer">1</container>
        <container type="folder" label="Folder">25-27</container>
        <unittitle>Miscellaneous (single family residences) (No Job No.)</unittitle>
        <physdesc>
            <extent>ca. 50 drawings</extent>
        </physdesc>
        <physdesc>
            <physfacet>pencil and ink on paper and cardboard, water color on cardboard, photostats</physfacet>
        </physdesc>
    </did>
    <odd>
        <p>(Renderings)</p>
    </odd>
</c03>
```

will become this:

```xml
<c03 level="file">
    <did>
        <unittitle>Miscellaneous (single family residences) (No Job No.)</unittitle>
        <physdesc>
            <extent>ca. 50 drawings</extent>
        </physdesc>
        <physdesc>
            <physfacet>pencil and ink on paper and cardboard, water color on cardboard, photostats</physfacet>
        </physdesc>
    </did>
    <odd>
        <p>(Renderings)</p>
    </odd>
    <c04 level="file">
        <did>
            <unittitle>Miscellaneous (single family residences) (No Job No.)</unittitle>
            <container type="box" label="Drawer">1</container>
            <container type="folder" label="Folder">25</container>
        </did>
    </c04>
    <c04 level="file">
        <did>
            <unittitle>Miscellaneous (single family residences) (No Job No.)</unittitle>
            <container type="box" label="Drawer">1</container>
            <container type="folder" label="Folder">26</container>
        </did>
        <odd>
            <p>(continued)</p>
        </odd>
    </c04>
    <c04 level="file">
        <did>
            <unittitle>Miscellaneous (single family residences) (No Job No.)</unittitle>
            <container type="box" label="Drawer">1</container>
            <container type="folder" label="Folder">27</container>
        </did>
        <odd>
            <p>(continued)</p>
        </odd>
    </c04>
</c03>
```

##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Usage
Change the path to the input directory defined in ```find_container_ranges.py``` to suit your own needs. 

Also if there are any EADs you would like the script to skip, add their filenames to the ```eads_to_skip``` list in the same script file.

Then just run it!