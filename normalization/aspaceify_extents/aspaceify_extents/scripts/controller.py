import os

from tqdm import tqdm

import etree_editor
from utilities.ead_utilities import ead_utilities as util
from extent_parser import split_into_extents
from make_aspace_extent_distinctions import split_into_aspace_components


def split_extents(ead):
    physdescs = ead.tree.xpath("//physdesc")
    for physdesc in physdescs:
        process_physdesc(ead, physdesc)

    return ead


def process_physdesc(ead, physdesc):
    tags = [tag.tag for tag in list(physdesc)]

    # don't split if there isn't an extent or physdesc tag
    if "extent" not in tags or "physdesc" in tags:
        return ead

    # don't split if it looks like we've already processed it
    if physdesc.get("altrender", ""):
        return ead

    extents = physdesc.xpath("//extent")

    for extent in extents:
        process_extent(ead, extent)

    # remove old physdescs
    physdesc.getparent().remove(physdesc)

    return ead


def process_extent(ead, extent):
    if extent.getparent().get("altrender", ""):
        return ""

    portion = extent.getparent().get("altrender", "")

    # get extent text
    text = extent.text if extent.text else ""

    # split into individual extent statements
    highlevel_extents = split_into_extents(text)
    is_multiple_extents = True if len(highlevel_extents) > 1 else False

    # create aspace components for each individual extent
    aspace_components = [split_into_aspace_components(extent_text, portion, is_multiple_extents) for extent_text in highlevel_extents]

    # add new tags to the ead tree
    etree_editor.make_aspace_formatted_physdesc(ead.tree, ead.tree.getpath(extent.getparent().getparent()), aspace_components)

    # remove old tags
    extent.getparent().remove(extent)


if __name__ == "__main__":
    # set up the ead directory object
    e = util.EADDir(input_dir=r"C:\Users\wboyle\PycharmProjects\without-reservations\Real_Masters_all")

    # run through each ead file in the directory
    for ead_file in tqdm(list(e.ead_files)):

        # make EAD object
        ead_ = util.EAD(os.path.join(e.input_dir, ead_file))

        # split the extents
        ead_ = split_extents(ead_)

        # [bit of a hack]
        # for some reason some of the physdescs are being left empty. This deletes them.
        for physdesc in ead_.tree.xpath("//physdesc"):
            if len(physdesc) == 0:
                physdesc.getparent().remove(physdesc)

        # prettyprint results
        ead_.prettyprint(output_dir=r"C:\Users\wboyle\PycharmProjects\without-reservations\Real_Masters_all")
