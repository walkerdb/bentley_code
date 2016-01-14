from lxml import etree
from utilities import EADDir


def add_aspace_ids_to_all_agents_in_dir(name_to_id_map, path_to_eads):
    ead_dir = EADDir(input_dir=path_to_eads)
    ead_dir.apply_function_to_dir(function=add_aspace_ids_to_agents, var1=name_to_id_map, output_dir=path_to_eads)


def add_aspace_ids_to_agents(ead_object, name_to_id_map):
    tree = ead_object.tree
    agents = tree.xpath("//controlaccess/*") + tree.xpath("//origination/*")
    for agent in agents:
        if agent.tag not in ["corpname", "famname", "persname"]:
            continue

        agent_text_base = unicode(agent.text.replace("---", "- --").strip().split("--")[0])
        agent_texts = [agent_text_base, u"{}.".format(agent_text_base), agent_text_base.rstrip(u"."), agent_text_base.rstrip(u". "), agent_text_base.strip()]

        found = False
        for agent_text in agent_texts:
            if agent_text in name_to_id_map:
                if not name_to_id_map[agent_text]:
                    print("??? {} -- {}".format(agent_text, etree.tostring(agent)))
                agent.attrib["ref"] = name_to_id_map[agent_text]
                found = True
        if not found:
            print("agent not in map! {}".format(agent_text_base.encode("utf-8")))
