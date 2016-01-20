from normalization.authority_reconciliation.scripts.false_positive_check import filter_out_false_positives
from normalization.authority_reconciliation.scripts.grab_all_subjects import grab_all_subjects
from normalization.authority_reconciliation.scripts.auth_search import AuthoritySearcher
from normalization.authority_reconciliation.scripts.write_new_lc_ids import write_new_lc_ids

# NOTE: This script will take ~8-9 hours to run, almost entirely due to required 2-second delays between web requests
# the script can run quite happily overnight.

# Define the EAD input and output directories. Generally we want to overwrite the files in the input directory,
# so we've set the output and input directories to be the same by default.
input_directory = "C:\path\to\your\ead\directory"
output_directory = input_directory

# Grab all subject terms
subjects = grab_all_subjects(input_directory)

# retrieve lc authorized names for each subject, if there is one
subjects_with_lc_terms = AuthoritySearcher().get_lc_authorized_names(subjects=subjects)

# filter out the false positives
subjects_without_false_positives = filter_out_false_positives(subjects_with_lc_terms)

# add new data to old eads
write_new_lc_ids(subjects_without_false_positives, input_directory, output_directory)
