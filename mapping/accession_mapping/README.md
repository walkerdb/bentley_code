#Accession mapping
A set of scripts for mapping and posting accession data from BEAL exports to an ASpace instance

##Setup
Requires [tqdm](https://github.com/noamraph/tqdm) and the [PySpace interface](https://github.com/walkerdb/bentley_code/blob/master/utilities/aspace_interface/pyspace.py)

Things to do and edit before running the code:

1. Use Dallas' BEAL export scripts to create a csv of original accession data from BEAL
2. Update the "input_filename" variable at the top of the ```accession_mapping.py``` script to the path to the intended input csv file
3. Update the PySpace connection code in ```accession_posting.py``` with the data for your local ASpace instance
4. If your instance of the PySpace code is stored somewhere else, be sure to update its import path in ```accession_posting.py```.

##Usage

1. Run ```accession_mapping.py```. This should create a "json_data.json" file in the script's directory
2. Run ```accession_posting.py```. This will take some time, and will print out the json response from ASpace if the post fails for any reason. Once it finishes all accessions should now be in your ASpace instance.