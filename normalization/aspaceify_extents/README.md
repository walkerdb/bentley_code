#Transformaing and normalizing EAD extent statements
This set of scripts performs the following:

1. Splits long-form extent statements containing multiple parts into individual extent statements
    * For example, an extent tag that was originally something like "10 photographs, 12 maps, and 5 golden rings" is split into three separate extent statements.
2. Splits each new atomized extent statement into the component parts expected by ArchivesSpace, normalizing all terms along the way. 

To give an example, an original statement like this:

```xml
<physdesc>
    <extent>5 cassette tapes (30 min.) and 10 CD-ROMs (in 2 folders)</extent>
</physdesc>
```

would be split and normalized into the following:

```xml
<physdesc>
    <extent altrender="materialtype spaceoccupied">5 audiocassettes</extent>
    <dimensions>30 minutes</dimensions>  <!-- the dimensions tag is used for either time or physical dimensions -->
</physdesc>
<physdesc>
    <extent altrender="materialtype spaceoccupied">10 optical disks</extent>  <!-- the extent type and count -->
    <extent altrender="carrier">in 2 folders</extent>  <!-- the thing containing the described objects -->
    <physfacet>CD-ROMs</physfacet>  <!-- details about the overarching extent type -->
</physdesc>
```
    
A full list of which terms are normalized into what can be found [here](https://docs.google.com/spreadsheets/d/1oen1UAFLzrATjVxHDlC7LRHHHaxeRpXsUTt0GhEKV1Y/edit#gid=0).

All terms are pluralized to enable better faceting in ArchivesSpace

The intent of this process is to facilitate the eventual generation of comprehensive extent reports from within ASpace.

##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Setup

Edit the ead path variables in ```run_aspaceify.py``` to the paths on your own computer

##Use
Just run ```run_aspaceify.py```! New EAD files with corrected extents will appear wherever you specified the output to be placed.