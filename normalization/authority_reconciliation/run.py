from normalization.authority_reconciliation.scripts.false_positive_check import filter_out_false_positives
from normalization.authority_reconciliation.scripts.grab_all_subjects import grab_all_subjects
from normalization.authority_reconciliation.scripts.auth_search import AuthoritySearcher

# Define the EAD input directory
ead_directory = r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all"

# Grab all subject terms
subjects = grab_all_subjects(ead_directory)

# retrieve lc authorized names for each subject, if there is one
subjects_with_lc_terms = AuthoritySearcher().get_lc_authorized_names(subjects=subjects)

# filter out the false positives
subjects_without_false_positives = filter_out_false_positives(subjects_with_lc_terms)

# add new data to old eads
# TODO implement this