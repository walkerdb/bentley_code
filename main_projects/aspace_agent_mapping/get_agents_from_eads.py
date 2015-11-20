import os

from lxml import etree
from tqdm import tqdm
from utilities import EADDir


def get_all_agents(input_dir):
    agent_types = ["corpname", "persname", "famname"]
    agents = dict(zip(agent_types, [{}, {}, {}]))

    ead_dir = EADDir(input_dir=input_dir)

    for ead in tqdm(ead_dir.ead_files):
        tree = etree.parse(os.path.join(ead_dir.input_dir, ead))
        all_agents = get_agents_from_ead(tree)

        for key, value in all_agents.items():
            agents[key].update(value)

    return agents

def get_agents_from_ead(tree):
    agent_types = ["corpname", "persname", "famname"]
    results_dict = dict(zip(agent_types, [{}, {}, {}]))

    for agent_type in agent_types:
        tags = tree.xpath("//controlaccess/{}".format(agent_type)) + tree.xpath("//origination/{}".format(agent_type))

        for tag in tags:
            auth = tag.attrib.get("authfilenumber", "")
            source = tag.attrib.get("source")
            attribs = [auth, source]
            name = tag.text.encode("utf-8")

            if name in results_dict[agent_type]:
                if auth and not results_dict[agent_type][name]:
                    results_dict[agent_type][name] = attribs
            else:
                results_dict[agent_type][name] = attribs

    return results_dict


if __name__ == "__main__":
    pass





