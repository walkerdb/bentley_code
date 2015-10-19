from utilities.utilities import EADDir

ead_dir = EADDir()

def fix_portions(ead):
    for did in ead.tree.xpath("//did"):
        physdescs = did.xpath("physdesc")
        # if len(physdescs) > 1:
        #     if all([len(physdesc.xpath("extent")) > 0 for physdesc in physdescs]):
        #         for physdesc in physdescs:
        #             physdesc.attrib["altrender"] = "part"
        if len(physdescs) == 1:
            if any([tag.tag == "extent" for tag in list(physdescs[0])]):
                physdescs[0].attrib["altrender"] = "whole"


def fix_lone_container_summaries(ead):
    for did in ead.tree.xpath("//did"):
        physdescs = did.xpath("physdesc")
        if len(physdescs) <= 1:
            continue

        last_extent_altrender = ""
        for i, physdesc in enumerate(physdescs):
            if len(list(physdesc)) != 1:
                last_extent_altrender = ""
                continue

            if physdesc[0].tag != "extent":
                last_extent_altrender = ""
                continue

            attribute = physdesc[0].attrib.get("altrender")
            if last_extent_altrender != "materialtype spaceoccupied":
                last_extent_altrender = attribute
                continue

            if attribute != "carrier":
                last_extent_altrender = attribute
                continue

            # we can now assume we've narrowed it down to the case we're looking for
            physdescs[i - 1].append(physdesc[0])
            physdesc.getparent().remove(physdesc)
            last_extent_altrender = attribute


ead_dir.apply_function_to_dir(fix_portions, r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all")
