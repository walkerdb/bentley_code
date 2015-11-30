from tqdm import tqdm
from main_projects.aspace_agent_mapping.Corpname import Corpname
from main_projects.aspace_agent_mapping.Famname import Famname
from main_projects.aspace_agent_mapping.Persname import Persname


def prepare_agents(agent_dict):
    prepped_data = {}
    for key, dct in tqdm(agent_dict.items(), desc="creating aspace json"):
        prepped_data[key] = prepare_json_for_agent_type(key, dct)

    return prepped_data


def prepare_json_for_agent_type(agent_type, agent_dict):
    prepped_data = {}
    for name, auth_values in agent_dict.items():
        auth_id, auth_source = auth_values
        if agent_type == "corpname":
            prepped_data[name] = Corpname(name, auth_id, auth_source).get_aspace_json()
        if agent_type == "persname":
            prepped_data[name] = Persname(name, auth_id, auth_source).get_aspace_json()
        if agent_type == "famname":
            prepped_data[name] = Famname(name, auth_id, auth_source).get_aspace_json()

    return prepped_data