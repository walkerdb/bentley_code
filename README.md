#Code for the Bentley Historical Library
An overview of code developed to assist work at the Bentley Historical Library

The majority are tools for working with EAD files, but there are several other useful projects described as well.


##Utilities
Utility tools used in many of the other scripts. They may be necessary for other scripts to run.

* __[ASpace/python API interface](https://github.com/walkerdb/bentley_code/tree/master/utilities/aspace_interface)__: A python-based convenience interface for interacting with the ASpace API
* __[EAD utilities](https://github.com/walkerdb/bentley_code/tree/master/utilities/ead_utilities)__: Two convenience classes for working with EAD files. One wraps common functionality used with single EAD files into one place and the other allows easy access to performing actions on entire directories of EADs
* __[EAD cleanup](https://github.com/walkerdb/bentley_code/tree/master/utilities/ead_cleanup)__: Scripts for prettifying the Bentley's EADs

##Normalization / cleanup
Tools for cleaning and normalizing EAD data

* __[ASpaceify Extents](https://github.com/walkerdb/bentley_code/tree/master/normalization/aspaceify_extents)__: A large-scale script to split extents into component ASpace parts, normalize terms, and write them back to their original EAD files
* __[Authority Reconciliation](https://github.com/walkerdb/bentley_code/tree/master/normalization/authority_reconciliation)__: Script to reconcile our local controlaccess terms with those in the LCNAF
* __[Removing unitdates from unittitles](https://github.com/walkerdb/bentley_code/tree/master/normalization/unitdates_in_unittitles)__: Many unittitles had unitdates embedded in them, which ASpace blindly strips out without regard to context. This script pre-empts that with some slightly more intelligent removal logic.
* __[Cleaning empty unittitles](https://github.com/walkerdb/bentley_code/tree/master/normalization/empty_unittitle_fix)__: Our EADs originally had a number of empty unittitle fields. This fixed them.
* __[Attribute normalization](https://github.com/walkerdb/bentley_code/tree/master/normalization/attribute_normalization)__: Convenience script to normalize attribute values based on given criteria
* __[Container label normalization](https://github.com/walkerdb/bentley_code/tree/master/normalization/container_labels)__: Makes all container labels singular
* __[Expanding container ranges](https://github.com/walkerdb/bentley_code/tree/master/normalization/expand_container_ranges)__: Given a single c0x item described with a range of containers (eg boxes 1-10), this script creates individual c0x entries for each item in that original range.
* __[Extent extraction from unittitles](https://github.com/walkerdb/bentley_code/tree/master/normalization/unittitle_parentheticals)__: A number of unittitles included their extents as a parenthetical. This extracts those and creates their relevant extent tags

##Mapping data to ASpace
Tools to map data from one system to another

* __[Agents from EADs to ASpace](https://github.com/walkerdb/bentley_code/tree/master/mapping/aspace_agent_mapping)__: Extracts all agents from a directory of EAD files, generates ASpace-compliant JSON for all of them, then posts that data to an ASpace instance.
* __[Accessions from BEAL to ASpace](https://github.com/walkerdb/bentley_code/tree/master/mapping/accession_mapping)__: Transforms BEAL accession exports (as exported by Dallas' scripts) into ASpace JSON, the posts the transformed data.

##Summarizations / characterizations
Tools to summarize or characterize specific sets of data

* __[UMich publications in HathiTrust](https://github.com/bentley-historical-library/UMich_HathiTrust_Pub_Summaries)__: Summarizes all U-Michigan publications found in the HathiTrust's digital library by publication series
* __[Characterizing c0x series paths](https://github.com/walkerdb/bentley_code/tree/master/summarization/c0x_series_paths)__: Exports a list of all series paths with occurrence counts across all eads (eg Series -> File -> File -> Item)
* __[Summarizing all tag/attribute value pairs](https://github.com/walkerdb/bentley_code/tree/master/summarization/tag_attribute_counts)__: Exports a list of the counts of all pairs of tag/attribute values found in all eads.
* __[Self-nesting tag detection](https://github.com/walkerdb/bentley_code/tree/master/summarization/check_tag_nesting)__: Finds all instances of tags that have the same tag type as a child. 
* __Missing boxes check__: Finds potential missing boxes in a finding aid (for example, if in the entire finding aid there is box 1 and 3 but never a 2, this flags that EAD file)
