import csv
from pprint import pprint

from tqdm import tqdm

from utilities.aspace_interface.pyspace import PySpace


def post_agents_and_record_ids(agent_dict, host, username, password):
    name_to_aspace_ids_map = {}
    pyspace = PySpace(host=host, username=username, password=password)

    for agent_type, agent_dct in agent_dict.items():
        for name, json_data in tqdm(agent_dct.items(), desc="posting {}s...".format(agent_type)):
            aspace_agent_type = normalize_agent_type(agent_type)
            response = post_agent(pyspace, json_data, aspace_agent_type)

            name_to_aspace_ids_map[name] = extract_aspace_id(response)

    # write_name_dict_to_file(name_to_aspace_ids_map)

    return name_to_aspace_ids_map


def extract_aspace_id(returned_json):
    aspace_id = ""
    if not returned_json:
        return ""
    if u"created" in returned_json:
        aspace_id = returned_json[u"uid"]
    if u"error" in returned_json:
        if u"conflicting_record" in returned_json[u"error"]:
            aspace_id = returned_json[u"error"][u"conflicting_record"][0]
        else:
            print(returned_json)
    return aspace_id


def write_name_dict_to_file(name_to_aspace_ids_map):
    with open("local_to_aspace_agent_name_map.csv", mode="wb") as f:
        data = []
        for name, aspace_id in name_to_aspace_ids_map.items():
            data.append([name, aspace_id])

        writer = csv.writer(f)
        writer.writerow(["name", "aspace_id"])
        writer.writerows(data)


def normalize_agent_type(agent_type):
    if agent_type == "persname":
        return "people"
    if agent_type == "corpname":
        return "corporate_entities"
    if agent_type == "famname":
        return "families"
    else:
        print("??? {}".format(agent_type))


def post_agent(pyspace, json_data, agent_type):
    try:
        return pyspace.add_agent(json_data, agent_type=agent_type)
    except:
        pprint(json_data)