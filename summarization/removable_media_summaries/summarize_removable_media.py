from collections import Counter, OrderedDict
import cStringIO
import codecs
from copy import deepcopy
import json
import csv
import os
from pprint import pprint
import re

from tqdm import tqdm
from lxml import etree

from utilities.ead_utilities.ead_utilities import EADDir, EAD

with open("locations.json", mode="r") as f:
    locations = json.load(f)


def main():
    digital_only = True
    ead_dir = EADDir(input_dir="path/to/your/ead/files")

    results_by_ead, all_extents = get_raw_results(ead_dir, digital_only)

    summary_by_type = summarize_results_by_type(deepcopy(results_by_ead))
    summary_by_ead = summarize_results_by_ead(deepcopy(results_by_ead))

    write_removable_media_inventory(all_extents)
    write_type_summary(summary_by_type, digital_only)
    write_ead_summary(summary_by_ead, digital_only)


def make_output_row(physdesc, ead_id):
    # TO ADD A NEW COLUMN IN THE INVENTORY OUTPUT:
    # make a new variable (eg: new_thing = make_new_thing(physdesc))
    # ("physdesc" is the lxml etree tag passed to the make_output_row function)
    #
    # then add that variable to the return statement
    # the order of variables in the return statement is the order the columns will appear in the output csv file
    # make sure to add the appropriate header entry in the write_removable_media_inventory() function (should be just below this one)

    extent_text = get_child_text(physdesc, "extent")
    number, extent_type = split_extent(extent_text)
    if number == 0:
        number = "[no number given]"

    physfacet_text = get_child_text(physdesc, "physfacet")
    containers = get_containers(physdesc)
    container_text = create_container_text(containers)
    uuid = get_uuid(physdesc)
    restriction, restrict_date = get_restriction(physdesc)
    breadcrumb_path = make_unittitle_breadcrumbs(physdesc)
    date_of_material = get_possible_material_date(physdesc)
    size = get_size(extent_text, physfacet_text)
    location = get_location(ead_id, containers)
    is_a_digitization = "yes" if is_digitized(physdesc) else ""
    digital_object_text = get_digital_object_siblings(physdesc)

    return number, extent_type, physfacet_text, size, location, container_text, date_of_material, digital_object_text, is_a_digitization, restriction, restrict_date, uuid, breadcrumb_path


def write_removable_media_inventory(all_extents):
    # if you've added any new columns in the make_output_row() function, be sure to add the appropriate header, in the right order, here

    headers = ["ead name", "ead id", "collection name", "number of items", "extent type", "physfacet text",
               "size (mb)", "location", "container", "potential date of material",
               "title of potentially related digital content (if any)",
               "is the result of a Bentley digitization project",
               "access restrictions", "access restiction dates", "uuid", "unittitle breadcrumb"]

    with open("removable_media_inventory.csv", mode="wb") as f:
        writer = UnicodeWriter(f)
        writer.writerow(headers)
        writer.writerows(all_extents)


def write_type_summary(results_summarized, digital_only):
    # make the data into a list where every entry is in the following form:
    # ((extent type, extent subtype), (total count, Counter dict with counts of thing in each EAD))
    data = sorted(results_summarized.items())
    with open("removable_media_summary_by_type.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerow(["media type", "media subtype", "total count", "counts by EAD"])
        for item in data:
            extent_type = item[0][0]
            if digital_only and extent_type != "digital":
                continue
            counts_by_ead = "\n".join(["{}: {}".format(thing[0], int(thing[1])) for thing in item[1][1].most_common()])
            row = [item[0][0], item[0][1], item[1][0], counts_by_ead]
            writer.writerow(row)


def write_ead_summary(summary_by_ead, digital_only):
    # TODO - write this. Serialize the dictionary and make sure you give default values to keys that might not exist in a given Counter.
    digital_keys = [("digital", "CDs"),
                    ("digital", "DVDs"),
                    ("digital", "USB thumb drives"),
                    ("digital", 'floppy disks: 3.5"'),
                    ("digital", 'floppy disks: 5.25"'),
                    ("digital", "floppy disks: size not known"),
                    ("digital", "magneto-optical disks"),
                    ("digital", "zip disks")]
    video_keys = [('video', '(type not listed)'),
                  ('video', '8mm videocassettes'),
                  ('video', 'Betacam tapes'),
                  ('video', 'Sony DVCAM videocassettes'),
                  ('video', 'U-matic tapes'),
                  ('video', 'VHS tapes'),
                  ('video', 'film reels'),
                  ('video', 'mini-DV tapes'),
                  ('video', 'open reel videotapes'),
                  ('video', '2-inch videotapes'),
                  ('video', '1-inch videotapes'),
                  ("video", "videocassette (unknown type)"),
                  ("video", "(unknown video type)"),
                  ('video', 'oversize')]
    audio_keys = [('audio', 'audiocassettes'),
                  ('audio', 'microcassettes'),
                  ('audio', 'phonograph records'),
                  ('audio', 'reel-to-reel tapes'),
                  ("audio", "wire recordings")]

    if digital_only:
        keys = digital_keys
    else:
        keys = digital_keys + video_keys + audio_keys


    # initialize empty values and setup dict for writing
    ead_dir = EADDir()
    for ead_file, counter in summary_by_ead.items():
        for key in keys:
            if key not in counter:
                counter[key] = 0
        for key in counter.keys():
            counter[u"{}: {}".format(unicode(key[0]), unicode(key[1]))] = counter[key]
            del counter[key]

        counter[u"collection name"] = EAD(os.path.join(ead_dir.input_dir, ead_file)).title
        summary_by_ead[ead_file] = counter

    # write
    with open("removable_media_summary_by_ead.csv", mode="wb") as f:
        # headers = [u"collection name", u"CDs", u"DVDs", u"USB thumb drives", u'floppy disks: 3.5"',
        #            u'floppy disks: 5.25"', u"floppy disks: size not known", u"magneto-optical disks", u"zip disks"]
        headers = [u"{}: {}".format(key[0], key[1]) for key in keys]
        headers.insert(0, u"collection name")
        writer = DictUnicodeWriter(f, fieldnames=headers)
        writer.writeheader()
        data = sorted(summary_by_ead.items())
        for name, counter in data:
            writer.writerow(counter)

    pass


def summarize_results_by_ead(results_by_ead):
    for ead_file, counter in results_by_ead.items():
        # clean up the counter
        normalize_counter_values(counter)
        results_by_ead[ead_file] = counter
    return results_by_ead


def summarize_results_by_type(results_by_ead):
    results = {}
    for ead_file, counter in results_by_ead.items():
        # clean up the counter
        normalize_counter_values(counter)
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


def get_raw_results(ead_dir, digital_only):
    results_by_ead = {}
    all_extents = []
    for ead_file in tqdm(ead_dir.ead_files):
        ead = EAD(os.path.join(ead_dir.input_dir, ead_file))

        summarized_results, all_results = find_removable_media(ead, digital_only)
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


def normalize_counter_values(counter):
    mappings = {"cd": ("digital", "CDs"),
                "dvd": ("digital", "DVDs"),
                "magneto-optical": ("digital", "magneto-optical disks"),
                "film": ("video", "film reels"),
                "16 mm": ("video", "film reels"),
                "16mm": ("video", "film reels"),
                "in. videotape": ("video", "2-inch videotapes"),
                "2-inch video": ("video", "2-inch videotapes"),
                "1-inch video": ("video", "1-inch videotapes"),
                "open reel videotape": ("video", "open reel videotapes"),
                "videocassette": ("video", "videocassette (unknown type)"),
                "videotape": ("video", "(unknown video type)"),
                "reel-to-reel": ("audio", "reel-to-reel tapes"),
                "reel to reel": ("audio", "reel-to-reel tapes"),
                "ips": ("audio", "reel-to-reel tapes"),
                "cassette tape": ("audio", "audiocassettes"),
                "phonograph": ("audio", "phonograph records"),
                "audiotapes": ("audio", "reel-to-reel tapes"),
                "audio-cassette": ("audio", "audiocassettes"),
                "audio cassette": ("audio", "audiocassettes"),
                "audio reel": ("audio", "reel-to-reel tapes"),
                "audio-tape": ("audio", "reel-to-reel tapes"),
                "audiotape": ("audio", "reel-to-reel tapes"),
                "wire recording": ("audio", "wire recordings"),
                "inch audio tape": ("audio", "reel-to-reel tapes"),
                "vhs": ("video", "VHS tapes"),
                "beta": ("video", "Betacam tapes"),
                "u-matic": ("video", "U-matic tapes"),
                "mini-dv": ("video", "mini-DV tapes")}

    for extent_physfacet_tuple, count in counter.items():
        extent, physfacet = extent_physfacet_tuple

        disallowed_keywords = ["mp4", "m4v", "mpeg4", "mpeg-4", 'video file', ".zip file", ".wav file", "mov file", "quicktime", "video paper", "includes video"]
        if any(keyword in "{} {}".format(extent, physfacet).lower() for keyword in disallowed_keywords):
            del counter[extent_physfacet_tuple]

        if extent == "audiocassettes" and physfacet != "microcassettes":
            new_key = ("audio", "audiocassettes")
            normalize_counter_entry(counter, new_key, extent_physfacet_tuple, count)

        if extent == "audiocassettes" and physfacet == "microcassettes":
            new_key = ("audio", "microcassettes")
            normalize_counter_entry(counter, new_key, extent_physfacet_tuple, count)

        if "audiocassette" in physfacet:
            new_key = ("audio", "audiocassettes")
            normalize_counter_entry(counter, new_key, extent_physfacet_tuple, count)

        if extent == "floppy disks":
            if not physfacet:
                physfacet = "size not known"

            new_key = ("digital", "{}: {}".format(extent, physfacet))
            normalize_counter_entry(counter, new_key, extent_physfacet_tuple, count)

        if extent == "videotapes":
            if not physfacet:
                physfacet = "(type not listed)"

            new_key = ("video", physfacet)
            normalize_counter_entry(counter, new_key, extent_physfacet_tuple, count)

        if extent == "zip disks":
            new_key = ("digital", "zip disks")
            normalize_counter_entry(counter, new_key, extent_physfacet_tuple, count)

        if extent == "USB thumb drives":
            new_key = ("digital", "USB thumb drives")
            normalize_counter_entry(counter, new_key, extent_physfacet_tuple, count)

            # if extent == "audiocassettes":
            #     k = ("audio", physfacet)
            #     normalize_counter_entry(counter, k, key, value)

    for extent_physfacet_tuple, count in counter.items():
        extent, physfacet = extent_physfacet_tuple

        for search_key, normalized_pair in mappings.items():
            if search_key in "{} {}".format(physfacet.lower(), extent.lower()):
                counter[normalized_pair] = counter.get(normalized_pair, 0) + count
                del counter[extent_physfacet_tuple]


def normalize_counter_entry(counter, key_to_add_original_value_to, original_key, count):
    counter[key_to_add_original_value_to] = counter.get(key_to_add_original_value_to, 0) + count
    del counter[original_key]


def find_removable_media(ead, digital_only):
    digital_extent_types = ["optical disks", "floppy disks", "USB thumb drives", "zip disks", "diskettes", "CD", "DVD", "magneto-optical disks"]
    digital_physfacet_keywords = ["CD", "DVD", "compact disk", "thumb drive"]

    analog_video_extent_types = ["videotapes", "videocassettes", "film"]
    analog_video_physfacet_keywords = ["beta", "vhs", "video", "16mm", "u-matic", "umatic", "mini-dv"]

    analog_audio_extent_types = ["audiocassettes", "audiotapes", "phonograph records", "wire recordings", "audiorecordings"]
    analog_audio_physfacet_keywords = ["reel-to-reel", "reel to reel", 'ips', 'microcassettes', 'cassette tape', 'audiocassette', 'audio cassette', "audio"]

    if digital_only:
        extent_types = digital_extent_types
        physfacet_keywords = digital_physfacet_keywords
    else:
        extent_types = digital_extent_types + analog_video_extent_types + analog_audio_extent_types
        physfacet_keywords = digital_physfacet_keywords + analog_video_physfacet_keywords + analog_audio_physfacet_keywords

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


def get_containers(physdesc):
    container = search_up_for_did_element(physdesc, "container")
    if not type(container) == etree._Element:
        return []

    container_data = []
    containers = [cont for cont in list(container.getparent()) if cont.tag == "container"]
    for container in containers:
        container_data.append((container.attrib["type"], container.text))

    return container_data


def get_uuid(physdesc):
    c0x_parent = physdesc.getparent().getparent()
    return c0x_parent.get("id", "")


def make_unittitle_breadcrumbs(physdesc):
    breadcrumbs = []

    is_c01 = False
    parent = physdesc.getparent().getparent()
    while not is_c01:
        unittitle = parent.xpath("did/unittitle")[0]
        unittitle_text = extract_text(unittitle)
        breadcrumbs.append(unicode(unittitle_text.strip()))

        if parent.tag == "c01" or parent.tag == "archdesc":
            is_c01 = True

        parent = parent.getparent()

    breadcrumbs.reverse()
    return u" -> ".join(breadcrumbs)


def get_location(ead_id, containers):
    container_type = ""
    container_number = ""
    for cont_type, cont_number in containers:
        if cont_type.lower() != "box":
            continue
        container_type = cont_type
        container_number = cont_number

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
                location = " to ".join(
                    list(filter(None, [loc_row["location start"].upper(), loc_row["location end"].upper()])))

    return location


def create_container_text(containers):
    if not containers:
        return "[container not listed]"
    texts = []
    for container_type, container_text in containers:
        texts.append("{} {}".format(container_type, container_text))

    return ", ".join(texts)


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


def is_digitized(physdesc):
    unittitle_text = get_sibling_text(physdesc, "unittitle").lower()
    physfacet_text = get_child_text(physdesc, "physfacet").lower()

    digitized_signifiers = ["use copy", "digitized", "converted", "transfer"]

    if any(signifier in unittitle_text or signifier in physfacet_text for signifier in digitized_signifiers):
        return True

    return False


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

    return ""


def get_digital_object_siblings(physdesc):
    parent_c0x = physdesc.getparent().getparent()
    if not parent_c0x.tag.startswith("c0"):
        return u""

    siblings = parent_c0x.getparent().xpath(parent_c0x.tag)
    index = siblings.index(parent_c0x)

    if index + 1 == len(siblings):
        return u""

    next_sibling = siblings[index + 1]

    sibling_unittitle_text = extract_text(next_sibling.xpath("did/unittitle")[0])
    physfacet_text = get_child_text(next_sibling, "did/physdesc/physfacet")

    file_extension_regex = re.compile(r"[a-zA-Z]\.[a-z]{3}\b")
    keyword_regexes = [file_extension_regex, re.compile(r"[sS]treaming")]

    if any(re.search(regex, sibling_unittitle_text) or re.search(regex, physfacet_text) for regex in keyword_regexes):
        if physfacet_text:
            sibling_unittitle_text = u"{} ({})".format(sibling_unittitle_text, physfacet_text)

        if "flv" in sibling_unittitle_text or "streaming" in sibling_unittitle_text.lower():
            sibling_unittitle_text = u"{}. Files are likely stored in R:\\Digitization\\Video".format(
                sibling_unittitle_text)

        return sibling_unittitle_text

    return ""


def search_up_for_did_element(physdesc, relative_tag_xpath):
    parent_did = physdesc.getparent()

    element = parent_did.xpath(relative_tag_xpath)

    while not element:
        try:
            parent_did = parent_did.getparent().getparent().xpath("did")[0]
            element = parent_did.xpath(relative_tag_xpath)
        except(IndexError, AttributeError):
            return ""

    return element[0]


def extract_years(date_text):
    year_regex = re.compile(r"\d{4}")
    return "-".join(re.findall(year_regex, date_text))


def extract_text(tag):
    text = etree.tostring(tag)
    tag_regex = re.compile(r"</?.*?>")
    extracted_text = " ".join(re.sub(tag_regex, "", text).split()).strip()

    return extracted_text if extracted_text else ""


def get_sibling_text(element, sibling_name):
    sibling = element.getparent().xpath(sibling_name)
    if not sibling:
        return ""

    return extract_text(sibling[0])


def get_child_text(element, child_name):
    children = element.xpath(child_name)
    if not children:
        return ""

    return extract_text(children[0])


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


class DictUnicodeWriter(object):
    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        new_dict = {}
        for k, v in D.items():
            if type(v) == str or type(v) == unicode:
                new_dict[k] = v.encode("utf-8")
            else:
                new_dict[k] = v

        self.writer.writerow(new_dict)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()


if __name__ == "__main__":
    main()
