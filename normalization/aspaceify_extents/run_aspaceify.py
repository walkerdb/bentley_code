from __future__ import absolute_import

from normalization.aspaceify_extents.aspaceify_extents import aspaceify_extents
from normalization.aspaceify_extents.aspaceify_extents.scripts.extent_grab import get_all_extents


# CHANGE THESE TWO PATHS TO MATCH YOUR SYSTEM
# THE OUTPUT DIRECTORY CAN BE ANYWHERE YOU'D LIKE
ead_input_directory = "path/to/ead/directory"
ead_output_directory = "path/to/where/you'd/like/new/eads/written/to"


# get a list of all extents in your eads, with their xml paths
extents = get_all_extents(ead_input_directory)


# now process this list
aspaceify_extents.main(extent_list=extents,
                       path_to_eads=ead_input_directory,
                       path_to_output=ead_output_directory)

