import csv
import nameparser
from mapping.aspace_agent_mapping.agent_parsers.Corpname import Corpname
from mapping.aspace_agent_mapping.agent_parsers.Persname import Persname


def construct_donor_name(row):
    pass


def main():
    convert_to_utf8_and_add_headers("donor_records.tab")
    donor_data = load_donor_data("donor_records_clean.tab")
    persname_data, corpname_data = extract_agents(donor_data)

    for persname in persname_data:
        full_name = make_person_name(persname)
        person_json = Persname(full_name, "", "local")
        # now do something with it
        pass

    for corpname in corpname_data:
        name = make_corporation_name(corpname)
        corp_json = Corpname(name, "", "local")
        # now do something with it




    pass


def load_donor_data(filepath):
    with open(filepath, mode="r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def extract_agents(donor_data):
    corporations = []
    people = []
    for donor in donor_data:
        if donor["last name"] and donor["organization"]:
            corporations.append(donor)
            people.append(donor)
        elif donor["last name"]:
            people.append(donor)
        elif donor["organization"]:
            corporations.append(donor)

    return people, corporations


def make_person_name(person):
    name = nameparser.HumanName()
    name.title = person["title"]
    name.first = person["first name"]
    name.middle = person["middle name"]
    name.last = person["last name"]
    name.suffix = person["suffix"]

    return unicode(name)


def make_corporation_name(corp):
    return unicode(corp['organization'])


def convert_to_utf8_and_add_headers(filename):
    with open(filename, mode="rb") as f:
        data = f.read()

    data = data.decode("latin-1")
    data = data.encode("utf-8")

    name, extension = filename.split(".")
    with open("{}_clean.{}".format(name, extension), mode="wb") as f:
        headers = ["contact id", "bhl dart id", "suffix", "first name", "middle name", "last name", "title",
                   "organization", "note", "status", "donor number", "donor part", "folder status"]
        f.write("\t".join(headers) + "\n")
        f.write(data)


if __name__ == "__main__":
    main()

