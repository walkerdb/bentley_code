from normalization.authority_reconciliation.scripts.grab_all_subjects import grab_all_subjects

# Define the EAD input directory
ead_directory = r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all"

# Grab all subject terms
subjects = grab_all_subjects(ead_directory)

# query viaf to get LC IDs
# TODO modify the viaf API code to work this way

# query LC to get standard names

# if new names pass false positive check, add them to EADs