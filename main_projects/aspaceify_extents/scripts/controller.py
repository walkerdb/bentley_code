import os

from tqdm import tqdm

import etree_editor
from utilities import utilities as util
from extent_parser import split_into_extents
from make_aspace_extent_distinctions import split_into_aspace_components


def split_extents(ead):
    physdescs = ead.tree.xpath("//physdesc")
    for physdesc in physdescs:
        process_physdesc(ead, physdesc)

    return ead


def process_physdesc(ead, physdesc):
    tags = [tag.tag for tag in list(physdesc)]
    if "extent" not in tags or "physdesc" in tags:
        return ead

    extents = physdesc.xpath("//extent")

    for extent in extents:
        process_extent(ead, extent)

    physdesc.getparent().remove(physdesc)

    return ead


def process_extent(ead, extent):
    text = extent.text if extent.text else ""
    highlevel_extents = split_into_extents(text)
    is_multiple_extents = True if len(highlevel_extents) > 1 else False
    aspace_components = [split_into_aspace_components(extent_text, is_multiple_extents) for extent_text in
                         highlevel_extents]
    etree_editor.write_aspace_extent_tags(ead.tree, ead.tree.getpath(extent.getparent().getparent()), aspace_components)
    extent.getparent().remove(extent)


if __name__ == "__main__":
    e = util.EADDir()
    for ead_file in tqdm(list(e.ead_files)):
        ead_ = util.EAD(os.path.join(e.input_dir, ead_file))
        ead_ = split_extents(ead_)
        for physdesc in ead_.tree.xpath("//physdesc"):
            if len(physdesc) == 0:
                physdesc.getparent().remove(physdesc)
        ead_.prettyprint(output_dir="output")
