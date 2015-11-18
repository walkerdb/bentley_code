import os
import re
import csv
from collections import namedtuple

from nameparser import HumanName
from lxml import etree
from tqdm import tqdm


def grab_persnames(input_dir):
    eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
    persnames_dict = {}

    for ead in tqdm(eads):
        try:
            tree = etree.parse(os.path.join(input_dir, ead))
        except etree.XMLSyntaxError as e:
            print("Error in {0}: {1}".format(ead, e))
            continue

        persnames = tree.xpath("//controlaccess/persname") + tree.xpath("//origination/persname")
        for persname in persnames:
            auth = persname.attrib.get("authfilenumber", "")
            source = persname.attrib.get("source")
            attribs = [auth, source]
            name = persname.text.encode("utf-8")
            if name in persnames_dict:
                if auth and not persnames_dict[name]:
                    persnames_dict[name] = attribs
            else:
                persnames_dict[name] = attribs

    with open("persnames.csv", mode="wb") as f:
        writer = csv.writer(f)
        data = sorted([[name, attrib[1], attrib[0]] for name, attrib in persnames_dict.items()])
        writer.writerows(data)


def parse_persname(persname, source, auth):
    ParsedName = namedtuple("ParsedName",
                            ["title", "primary", "secondary", "suffix", "fuller_form", "birth_date", "death_date",
                             "auth", "source"])

    name = persname.split("--")[0]
    name, birth_date, death_date = extract_birth_death_dates(name)
    name = HumanName(name.decode("utf-8"))

    titles = ["sir", "mr", "mrs", "baron", "dame", "madame", "viscount", "conte"]
    title = name.title
    suffix = name.suffix

    # check if the suffix should actually be a title
    if not title and any(suffix.lower().strip(". ") == title for title in titles):
        title = suffix.capitalize()
        if "mr" in title.lower() and not title.endswith("."):
            title += "."
        suffix = u""

    # special cases cleanup
    if name.title == u"Royal":
        name.title = ""
        title = ""
        name.middle = name.first if not name.middle else "{} {}".format(u"Royal", name.middle)
        name.first = u"Royal"

    if name.title == u"Queen of Great":
        title = name.title + u" Britain"
        name.first = u""

    if name.title == u"Lama":
        title = u"Dalai Lama XIV"
        name.first = u""
        name.middle = u""

    name_parsed = ParsedName(
        title=title,
        primary=name.last,
        secondary=u"{0} {1}".format(name.first, name.middle).rstrip(),
        suffix=suffix,
        fuller_form=name.nickname,
        birth_date=birth_date,
        death_date=death_date,
        auth=auth,
        source=source)

    return name_parsed


def extract_birth_death_dates(string):
    alt_date_regex = r"(\d{4}) or \d{2}"
    date_regex = r"(\d{4})\??\-(?:ca\.)?((?:\d{4})?)\??"
    birth_letter_regex = r"b\. ?(\d{4})()"
    death_letter_regex = r"d\. ?()(\d{4})"
    circa_regex_1 = r"(\d{4}) \(ca\.\)-(\d{4})"
    birth_date = ""
    death_date = ""

    string = re.sub(alt_date_regex, "\g<1>", string)
    string = string.rstrip(".")

    for regex in [date_regex, birth_letter_regex, death_letter_regex, circa_regex_1]:
        dates = re.findall(regex, string)

        if len(dates) == 1:
            string = re.sub(regex, "", string)
            string = string.replace(" ca.", "").rstrip(" ,")
            birth_date, death_date = dates[0]
            break

    return string, birth_date, death_date


if __name__ == "__main__":
    input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    grab_persnames(input_dir)
    output = []
    with open("persnames.csv") as f:
        reader = csv.reader(f)
        for persname, source, auth in tqdm(list(reader)):
            n = parse_persname(persname, source, auth)
            output.append([persname, n.title.encode("utf-8"), n.primary.encode("utf-8"), n.secondary.encode("utf-8"),
                           n.suffix.encode("utf-8"), n.fuller_form.encode("utf-8"), n.birth_date, n.death_date, n.auth,
                           n.source])

    with open("parsed_persnames.csv", mode="wb") as f:
        headers = ["original name", "title", "primary", "secondary", "suffix", "fuller form", "birth date",
                   "death date", "auth link", "source"]
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(output)
