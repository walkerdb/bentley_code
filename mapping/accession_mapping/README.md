#Accession mapping
A set of scripts for mapping and posting accession data from BEAL exports to an ASpace instance

##Setup
Requires tqdm and the PySpace interface

##Usage

Before running the code:

1. Use Dallas' BEAL export scripts to create a csv of original accession data
2. Update the "input_filename" variable at the top of the ```accession_mapping.py``` script to the path to the intended input csv file
3. Update the PySpace connection code in ```accession_posting.py``` with the data for your local ASpace instance

Then perform the following

1. Run ```accession_mapping.py```. This should create a "json_data.json" file in the script's directory
2. Run ```accession_posting.py```. This will take some time. Once it finishes all accessions should now be in your ASpace instance.