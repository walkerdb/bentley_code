import codecs
from collections import Counter, OrderedDict
import csv
import cStringIO
import json
from lxml import etree
import os
from pprint import pprint
import re
from tqdm import tqdm

from utilities.ead_utilities.ead_utilities import EADDir, EAD


with open("locations.json", mode="r") as f:
    locations = json.load(f)


def main():
    ead_dir = EADDir()

    results_by_ead, all_extents = get_raw_results(ead_dir)
    results_summarized = create_summarized_results(results_by_ead)
    write_all_extents_to_csv(all_extents)
    write_summary_to_csv(results_summarized, digital_only=True)


def write_all_extents_to_csv(all_extents):
    with open("removable_media_inventory.csv", mode="wb") as f:
        writer = UnicodeWriter(f)

        headers = ["ead name", "ead id", "collection name", "number of items", "extent type", "physfacet text",
                   "size (mb)", "location", "container type", "container number", "potential date of material", "access restrictions",
                   "access restiction dates", "uuid", "unittitle breadcrumb"]
        writer.writerow(headers)
        writer.writerows(all_extents)


def write_summary_to_csv(results_summarized, digital_only):

    # make the data into a list where every entry is in the following form:
    # ((extent type, extent subtype), (total count, Counter dict with counts of thing in each EAD))
    data = sorted(results_summarized.items())
    with open("removable_media_summary.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerow(["media type", "media subtype", "total count", "counts by EAD"])
        for item in data:
            extent_type = item[0][0]
            if digital_only and extent_type != "digital":
                continue
            counts_by_ead = "\n".join(["{}: {}".format(thing[0], int(thing[1])) for thing in item[1][1].most_common()])
            row = [item[0][0], item[0][1], item[1][0], counts_by_ead]
            writer.writerow(row)

            # pprint(data)


def create_summarized_results(results_by_ead):
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
    return results


def extract_eadid(text):
    id_regex = re.compile(r"\d.*")
    return re.findall(id_regex, text)[0]


def get_raw_results(ead_dir):
    results_by_ead = {}
    all_extents = []
    for ead_file in tqdm(ead_dir.ead_files):
        ead = EAD(os.path.join(ead_dir.input_dir, ead_file))

        summarized_results, all_results = find_removable_media(ead)
        if summarized_results:
            results_by_ead[ead_file] = summarized_results

        if all_results:
            for result in all_results:
                result = list(result)
                if type(result[0]) is int:
                    number = result[0]
                    result[0] = 1
                    for i in range(number):
                        all_extents.append([ead.filename, ead.id, ead.title] + result)
                else:
                    all_extents.append([ead.filename, ead.id, ead.title] + result)

    return results_by_ead, all_extents


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


def get_child_text(element, child_name):
    children = element.xpath(child_name)
    if not children:
        return ""

    return children[0].text


def search_up_for_did_element(physdesc, relative_tag_xpath):
    parent_did = physdesc.getparent()

    element = parent_did.xpath(relative_tag_xpath)

    while not element:
        try:
            parent_did = parent_did.getparent().getparent().xpath("did")[0]
            element = parent_did.xpath(relative_tag_xpath)
        except (IndexError, AttributeError):
            return ""

    return element[0]


def get_container_info(physdesc):
    container = search_up_for_did_element(physdesc, "container")
    if not type(container) == etree._Element:
        return "[container not listed]", "[container not listed]"

    container_type = container.attrib["type"]
    container_number = container.text

    return container_type, container_number


def make_unittitle_breadcrumbs(physdesc):
    breadcrumbs = []

    is_c01 = False
    parent = physdesc.getparent().getparent()
    # print(etree.tostring(parent))
    while not is_c01:
        try:
            unittitle = parent.xpath("did/unittitle")[0]
            unittitle_text = extract_text(unittitle)
            breadcrumbs.append(unicode(unittitle_text.strip()))

        except IndexError:
            print(etree.tostring(parent))
            exit()

        if parent.tag == "c01" or parent.tag == "archdesc":
            is_c01 = True

        parent = parent.getparent()

    breadcrumbs.reverse()
    return u" -> ".join(breadcrumbs)


def get_uuid(physdesc):
    c0x_parent = physdesc.getparent().getparent()
    return c0x_parent.get("id", "")


def find_removable_media(ead):
    extent_types = ["optical disks", "floppy disks", "USB thumb drives", "zip disks", "diskettes", "CD", "DVD", "magneto-optical disks"]

    physfacet_keywords = ["CD", "DVD", "compact disk", "thumb drive"]

    media_counts = Counter()
    all_media = []

    physdescs = ead.tree.xpath("//physdesc")
    for physdesc in physdescs:
        extent_text = get_child_text(physdesc, "extent")
        physfacet_text = get_child_text(physdesc, "physfacet")

        if physfacet_text and not extent_text:
            if any(keyword in physfacet_text for keyword in physfacet_keywords):
                media_counts[("", physfacet_text)] = media_counts.get(("", physfacet_text), 0) + 1

                all_media.append(make_output_row(physdesc, ead.id))

        if extent_text:
            number, extent_text = split_extent(extent_text)
            if not any(extent_text == extent for extent in extent_types) or not number:
                continue

            media_counts[(extent_text, physfacet_text)] = media_counts.get((extent_text, physfacet_text), 0) + number
            all_media.append(make_output_row(physdesc, ead.id))

    return media_counts, all_media


def get_location(ead_id, container_type, container_number):
    location = ""
    if not container_number.isdigit():
        return ""

    container_number = int(container_number)

    if ead_id in locations:
        all_locations = locations[ead_id]["locations"]
        for loc_row in all_locations:
            if loc_row["location type"].lower() != container_type.lower():
                continue
            min_box = loc_row["box start"]
            max_box = loc_row["box end"] or min_box

            if not min_box and not max_box:
                continue

            if not min_box.isdigit():
                continue

            min_box = int(min_box)
            max_box = int(max_box)

            if container_number in list(range(min_box, max_box + 1)):
                location = " to ".join(list(filter(None, [loc_row["location start"].upper(), loc_row["location end"].upper()])))

    return location


def make_output_row(physdesc, ead_id):
    extent_text = get_child_text(physdesc, "extent")
    number, extent_type = split_extent(extent_text)
    if number == 0:
        number = "[no number given]"
    physfacet_text = get_child_text(physdesc, "physfacet")
    container_type, container_number = get_container_info(physdesc)
    uuid = get_uuid(physdesc)
    restriction, restrict_date = get_restriction(physdesc)
    breadcrumb_path = make_unittitle_breadcrumbs(physdesc)
    date_of_material = get_possible_material_date(physdesc)
    size = get_size(extent_text, physfacet_text)

    location = get_location(ead_id, container_type, container_number)

    return number, extent_type, physfacet_text, size, location, container_type, container_number, date_of_material, restriction, restrict_date, uuid, breadcrumb_path


def get_size(extent_text, physfacet_text):
    size_map = OrderedDict([("floppy", 1.4),
                            ("cd", 700),
                            ("dvd-ram", 5200),
                            ("dvd", 4700),
                            ("zip", 100),
                            ("magneto-optical", 1300)])

    for key in size_map:
        if key in extent_text.lower() or key in physfacet_text.lower():
            return size_map[key]

    return ""


def get_restriction(physdesc):
    text = ""
    date = ""

    accessrestrict = search_up_for_did_element(physdesc, "../accessrestrict")

    if type(accessrestrict) == etree._Element:
        text = extract_text(accessrestrict)
        accessrestriction_date = accessrestrict.xpath("p/date")
        if accessrestriction_date:
            date = accessrestriction_date[0].get("normal", accessrestriction_date[0].text)

    return text, date


def extract_text(tag):
    text = etree.tostring(tag)
    tag_regex = re.compile(r"</?.*?>")

    return " ".join(re.sub(tag_regex, "", text).split()).strip()


def get_possible_material_date(physdesc):
    date = search_up_for_did_element(physdesc, "unitdate")
    if type(date) == etree._Element:
        return extract_years(date.get("normal", date.text))

    date = search_up_for_did_element(physdesc, "unittitle/unitdate")
    if type(date) == etree._Element:
        return extract_years(date.get("normal", date.text))

    date = physdesc.getroottree().xpath("//archdesc/did/unittitle/unitdate")
    if type(date) == etree._Element:
        return extract_years(date[0].get("normal", date[0].text))

    return "no date found"


def extract_years(date_text):
    year_regex = re.compile(r"\d{4}")
    return "-".join(re.findall(year_regex, date_text))


def get_sibling_text(element, sibling_name):
    sibling = element.getparent().xpath(sibling_name)
    if not sibling:
        return ""

    return sibling[0].text


def split_extent(extent_text):
    try:
        number = int(float(extent_text.split(" ")[0]))
        text = extent_text.lstrip("1234567890-. ")

        return number, text

    except (IndexError, TypeError, ValueError):
        return 0, ""


class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") if type(s) == unicode else unicode(s).encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == "__main__":
    main()
