import csv
import json
import nameparser
from mapping.aspace_agent_mapping.agent_parsers.Corpname import Corpname
from mapping.aspace_agent_mapping.agent_parsers.Persname import Persname
from mapping.aspace_agent_mapping.scripts.post_agents import post_agents_and_record_ids


def main():
    convert_to_utf8_and_add_headers("donor_records.tab")
    donor_data = load_donor_data("donor_records_clean.tab")
    persname_data, corpname_data = extract_agents(donor_data)

    agent_dict = {"persname": {}, "corpname": {}}

    for persname in persname_data:
        full_name = make_person_name(persname)
        person_json = Persname(full_name, "", "local")

        # TODO add donor-specific data to the json

        agent_dict["persname"][full_name] = person_json

    for corpname in corpname_data:
        name = make_corporation_name(corpname)
        corp_json = Corpname(name, "", "local")

        # TODO add donor-specific data to the json

        agent_dict["corpname"][name] = corp_json

    ids = post_agents_and_record_ids(agent_dict, host="http://localhost:8089", username="admin", password="admin")

    with open("donor_name_to_aspace_id_map.json", mode="w") as f:
        json.dump(ids, f, ensure_ascii=False, indent=4)


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

