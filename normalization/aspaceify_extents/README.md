#Transformaing and normalizing EAD extent statements
This set of scripts performs the following:

1. Splits long-form extent statements containing multiple parts into individual extent statements
    * For example, an extent tag that was originally something like "10 photographs, 12 maps, and 5 golden rings" is split into three separate extent statements.
2. Splits each new atomized extent statement into the component parts expected by ArchivesSpace, normalizing all terms along the way. 

    An original statement like this:

    ```xml
    <physdesc>
        <extent>12 photographic negatives (12 x 10 in.) in 2 folders</extent>
    </physdesc>
    ```
    
    would be split into the following tags:

    ```xml
    <physdesc>
        <extent altrender="materialtype spaceoccupied">12 photographs</extent>  <!-- the extent type and count -->
        <extent altrender="carrier">in 2 folders</extent>  <!-- the thing containing the described objects -->
        <physfacet>photographic negatives</physfacet>  <!-- details about the overarching extent type -->
        <dimensions>12in. x 10in.</dimensions>  <!-- the physical size of the items -->
    </physdesc>
    ```
    
A full list of which terms are normalized into what can be found here.

All terms are pluralized to enable better faceting in ArchivesSpace

The intent of this process is to facilitate the eventual generation of comprehensive extent reports from within ASpace.

##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Setup

edit the ead path variables in ```run_aspaceify.py``` to the paths on your own computer

##Use
Just run ```run_aspaceify.py```! New EAD files with corrected extents will appear wherever you specified the output to be placed.