from collections import defaultdict

# TODO write prep code
# TODO persnames based on current parse_persname code
# TODO corp and famnames can be from Max's code

def prepare_agents(agent_dict):
    prepped_data = {}
    for key, dct in agent_dict.items():
        if key == "corpname":
            prepped_data[key] = prepare_corpnames(dct)
        if key == "persname":
            prepped_data[key] = prepare_persnames(dct)
        if key == "famname":
            prepped_data[key] = prepare_famnames(dct)

def prepare_persnames(persname_dict):
    pass

def prepare_corpnames(corpname_dict):
    pass

def prepare_famnames(famname_dict):
    pass
