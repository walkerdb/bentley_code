from collections import Counter
import os
from pprint import pprint
from lxml import etree
from tqdm import tqdm

from utilities.ead_utilities.ead_utilities import EADDir, EAD


def main():
    counter = Counter()
    ead_dir = EADDir()

    for ead_file in tqdm(ead_dir.ead_files):
        ead = EAD(os.path.join(ead_dir.input_dir, ead_file))
        counter += find_removable_media(ead)

    # cleaning up the counter
    for key, value in counter.items():
        extent, physfacet = key
        mappings = {"cd": "CDs",
                    "dvd": "DVDs",
                    "magneto-optical": "magneto-optical disks",
                    "film": "film reels",
                    "reel-to-reel": "reel-to-reel tapes",
                    "phonograph": "phonograph records",
                    "audiotapes": "reel-to-reel tapes",
                    "vhs": "VHS tapes",
                    "beta": "Betacam tapes",
                    "u-matic": "U-matic tapes",
                    "mini-dv": "mini-DV tapes"}

        for search_key, normalized_term in mappings.items():
            if search_key in physfacet.lower() or search_key in extent.lower():
                counter[(normalized_term, " ")] = counter.get((normalized_term, " "), 0) + value
                del counter[key]

        if physfacet and extent == "audiocassettes" and physfacet != "microcassettes":
            counter[("audiocassettes", "")] = counter.get(("audiocassettes", ""), 0) + value
            del counter[key]

    pprint(counter.most_common())


def find_removable_media(ead):
    extent_types = ["optical disks", "floppy disks", "USB thumb drives", "zip disks", "diskettes", "CD", "DVD", "magneto-optical disks", "audiocassettes", "film reels", "audiotapes", "phonograph records", "videotapes"]

    physfacet_keywords = ["CD", "DVD", "compact disk", "thumb drive", "film"]

    results = Counter()

    extents = ead.tree.xpath("//extent")
    for extent in extents:
        extent_text = extent.text
        number, extent_text = split_extent(extent_text)
        physfacet_text = get_sibling_text(extent, "physfacet")

        if not any(extent_text == extent for extent in extent_types) or not number:
            continue

        results[(extent_text, physfacet_text)] = results.get((extent_text, physfacet_text), 0) + number


    physfacets = ead.tree.xpath("//physfacet")
    for physfacet in physfacets:
        physfacet_text = physfacet.text
        extent_text = get_sibling_text(physfacet, "extent")
        if extent_text or not physfacet_text:
            continue

        if any(keyword in physfacet_text for keyword in physfacet_keywords):
            results[("", physfacet_text)] = results.get(("", physfacet_text), 0) + 1

    return results



def get_sibling_text(element, sibling_name):
    sibling = element.getparent().xpath(sibling_name)
    if not sibling:
        return ""

    return sibling[0].text


def split_extent(extent_text):
    try:
        number = float(extent_text.split(" ")[0])
        text = extent_text.lstrip("1234567890-. ")

        return number, text

    except (IndexError, TypeError, ValueError):
        return 0, ""


if __name__ == "__main__":
    main()
