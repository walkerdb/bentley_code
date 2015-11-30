import csv
from main_projects.aspace_interface.pyspace import PySpace


def write_name_dict_to_file(name_to_aspace_ids_map):
    with open("local_to_aspace_agent_name_map.csv") as f:
        data = []
        for name, aspace_id in name_to_aspace_ids_map:
            data.append([name, aspace_id])

        writer = csv.writer(f)
        writer.writerow(["name", "aspace_id"])
        writer.writerows(data)

def post_agents_and_record_ids(agent_dict):
    name_to_aspace_ids_map = {}
    pyspace = PySpace()

    for agent_type, agent_dct in agent_dict.items():
        for name, json_data in agent_dct.items():
            agent_type = normalize_agent_type(agent_type)
            returned_json = post_agent(pyspace, json_data, agent_type)

            name_to_aspace_ids_map[u"name"] = extract_aspace_id(returned_json)

    write_name_dict_to_file(name_to_aspace_ids_map)


def extract_aspace_id(returned_json):
    aspace_id = ""
    if u"created" in returned_json:
        aspace_id = returned_json[u"uid"]
    if u"error" in returned_json:
        if u"conflicting_record" in returned_json[u"error"]:
            aspace_id = returned_json[u"error"][u"conflicting_record"][0]
        else:
            print(returned_json)
    return aspace_id


def normalize_agent_type(agent_type):
    if agent_type == "persname":
        return "people"
    if agent_type == "corpname":
        return "corporate_entities"
    if agent_type == "famname":
        return "families"


def post_agent(pyspace, json_data, agent_type):
    return pyspace.add_agent(json_data, agent_type=agent_type)