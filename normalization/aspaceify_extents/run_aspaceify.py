from __future__ import absolute_import

from normalization.aspaceify_extents.aspaceify_extents import aspaceify_extents
from normalization.aspaceify_extents.aspaceify_extents.scripts.extent_grab import write_extents_to_csv


# CHANGE THESE TWO PATHS TO MATCH YOUR SYSTEM
# THE OUTPUT DIRECTORY CAN BE ANYWHERE YOU'D LIKE
ead_input_directory = "path/to/ead/directory"
ead_output_directory = "path/to/where/you'd/like/new/eads/written/to"


# leave this one alone
path_to_extent_list_csv = "all_extents_reversed.csv"


# get a list of all extents in your eads, with their xml paths
write_extents_to_csv(ead_input_directory)


# now process this list
aspaceify_extents.main(source=path_to_extent_list_csv,
                       path_to_eads=ead_input_directory,
                       path_to_output=ead_output_directory)

