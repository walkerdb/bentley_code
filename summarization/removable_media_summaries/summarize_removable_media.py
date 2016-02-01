from collections import Counter
import csv
import os
from pprint import pprint
from tqdm import tqdm

from utilities.ead_utilities.ead_utilities import EADDir, EAD


def main():
    mappings = {"cd": ("digital", "CDs"),
                "dvd": ("digital", "DVDs"),
                "magneto-optical": ("digital", "magneto-optical disks"),
                "film": ("video", "film reels"),
                "reel-to-reel": ("audio", "reel-to-reel tapes"),
                "phonograph": ("audio", "phonograph records"),
                "audiotapes": ("audio", "reel-to-reel tapes"),
                "vhs": ("video", "VHS tapes"),
                "beta": ("video", "Betacam tapes"),
                "u-matic": ("video", "U-matic tapes"),
                "mini-dv": ("video", "mini-DV tapes")}
    results_by_ead = {}
    ead_dir = EADDir()

    for ead_file in tqdm(ead_dir.ead_files):
        ead = EAD(os.path.join(ead_dir.input_dir, ead_file))
        results_by_ead[ead_file] = find_removable_media(ead)

    results = {}
    for ead_file, counter in results_by_ead.items():
        # clean up the counter
        normalize_counter_values(counter, mappings)
        for key, value in counter.items():
            if key not in results:
                results[key] = (0, Counter())

            total_count, counts_by_ead = results[key]
            total_count += value
            counts_by_ead[ead_file] = value

            results[key] = (total_count, counts_by_ead)

    data = sorted(results.items())
    with open("output.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerow(["media type", "media subtype", "total count", "counts by EAD"])
        for item in data:
            counts_by_ead = "\n".join(["{}: {}".format(thing[0], int(thing[1])) for thing in item[1][1].most_common()])
            row = [item[0][0], item[0][1], item[1][0], counts_by_ead]
            writer.writerow(row)

    # pprint(data)


def normalize_counter_values(counter, mappings):
    for key, value in counter.items():
        extent, physfacet = key

        if extent == "audiocassettes" and physfacet != "microcassettes":
            k = ("audio", "audiocassettes")
            normalize_counter_entry(counter, k, key, value)

        if extent == "audiocassettes" and physfacet == "microcassettes":
            k = ("audio", "microcassettes")
            normalize_counter_entry(counter, k, key, value)

        if extent == "floppy disks":
            if not physfacet:
                physfacet = "size not known"

            k = ("digital", "{}: {}".format(extent, physfacet))
            normalize_counter_entry(counter, k, key, value)

        if extent == "videotapes":
            if not physfacet:
                physfacet = "(type not listed)"

            k = ("video", physfacet)
            normalize_counter_entry(counter, k, key, value)

        if extent == "zip disks":
            k = ("digital", "zip disks")
            normalize_counter_entry(counter, k, key, value)

        if extent == "USB thumb drives":
            k = ("digital", "USB thumb drives")
            normalize_counter_entry(counter, k, key, value)

            # if extent == "audiocassettes":
            #     k = ("audio", physfacet)
            #     normalize_counter_entry(counter, k, key, value)
    for key, value in counter.items():
        extent, physfacet = key
        for search_key, normalized_pair in mappings.items():
            ext, phys = normalized_pair
            if search_key in physfacet.lower() or search_key in extent.lower():
                counter[(ext, phys)] = counter.get((ext, phys), 0) + value
                del counter[key]


def normalize_counter_entry(counter, k, key, value):
    counter[k] = counter.get(k, 0) + value
    del counter[key]


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
