#Code for the Bentley Historical Library
An overview of code developed to assist work at the Bentley Historical Library

The majority are tools for working with EAD files, but there are several other useful projects described as well.


##Utilities
Utility tools used in many of the other scripts. They may be necessary for other scripts to run.

* __ASpace/python API interface__: A python-based convenience interface for interacting with the ASpace API
* __EAD utilities__: Two convenience classes for working with EAD files. One wraps common functionality used with single EAD files into one place and the other allows easy access to performing actions on entire directories of EADs
* __EAD cleanup__: Scripts for prettifying the Bentley's EADs

##Normalization / cleanup
Tools for cleaning and normalizing EAD data

* __ASpaceify Extents__: A large-scale script to split extents into component ASpace parts, normalize terms, and write them back to their original EAD files
* __Authority Reconciliation__: Script to reconcile our local controlaccess terms with those in the LCNAF
* __Removing unitdates from unittitles__: Many unittitles had unitdates embedded in them, which ASpace blindly strips out without regard to context. This script pre-empts that with some slightly more intelligent removal logic.
* __Cleaning empty unittitles__: Our EADs originally had a number of empty unittitle fields. This fixed them.
* __Attribute normalization__: Convenience script to normalize attribute values based on given criteria
* __Container label normalization__: Makes all container labels singular
* __Expanding container ranges__: Given a single c0x item described with a range of containers (eg boxes 1-10), this script creates individual c0x entries for each item in that original range.
* __Extent extraction from unittitles__: A number of unittitles included their extents as a parenthetical. This extracts those and creates their relevant extent tags

##Mapping data to ASpace
Tools to map data from one system to another

* __Agents from EADs to ASpace__: Extracts all agents from a directory of EAD files, generates ASpace-compliant JSON for all of them, then posts that data to an ASpace instance.
* __Accessions from BEAL to ASpace__: Transforms BEAL accession exports (as exported by Dallas' scripts) into ASpace JSON, the posts the transformed data.

##Summarizations / characterizations
Tools to summarize or characterize specific sets of data

* __UMich publications in HathiTrust__: Summarizes all U-Michigan publications found in the HathiTrust's digital library by publication series
* __Characterizing c0x series paths__: Exports a list of all series paths with occurrence counts across all eads (eg Series -> File -> File -> Item)
* __Summarizing all tag/attribute value pairs__: Exports a list of the counts of all pairs of tag/attribute values found in all eads.
* __Self-nesting tag detection__: Finds all instances of tags that have the same tag type as a child. 
* __Missing boxes check__: Finds potential missing boxes in a finding aid (for example, if in the entire finding aid there is box 1 and 3 but never a 2, this flags that EAD file)
