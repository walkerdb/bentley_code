import os

from tqdm import tqdm

import etree_editor
from utilities import utilities as util
from extent_parser import split_into_extents
from make_aspace_extent_distinctions import split_into_aspace_components


def split_extents(ead):
    physdescs = ead.tree.xpath("//physdesc")

    for physdesc in physdescs:
        tags = [tag.tag for tag in list(physdesc)]
        if "extent" not in tags or "physdesc" in tags:
            continue

        extents = physdesc.xpath("//extent")

        for extent in extents:
            text = extent.text if extent.text else ""
            highlevel_extents = split_into_extents(text)

            is_multiple_extents = True if len(highlevel_extents) > 1 else False
            aspace_components = [split_into_aspace_components(extent_text, is_multiple_extents) for extent_text in highlevel_extents]

            etree_editor.write_aspace_extent_tags(ead.tree, ead.tree.getpath(extent.getparent().getparent()), aspace_components)
            extent.getparent().remove(extent)

        physdesc.getparent().remove(physdesc)

    return ead

if __name__ == "__main__":
    e = util.EADDir()
    for ead_file in tqdm(list(e.ead_files)):
        ead = util.EAD(os.path.join(e.input_dir, ead_file))
        ead = split_extents(ead)
        ead.prettyprint(output_dir=e.input_dir)
