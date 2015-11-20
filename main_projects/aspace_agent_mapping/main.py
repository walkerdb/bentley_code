from main_projects.aspace_agent_mapping.get_agents_from_eads import get_all_agents
from main_projects.aspace_agent_mapping.post_agents import post_agents
from main_projects.aspace_agent_mapping.prepare_agents_for_aspace import prepare_agents

input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'

# extract agent data from eads
agents = get_all_agents(input_dir)

# create json-formatted entries for each agent
prepped_agents = prepare_agents(agents)

# send these formatted entries to aspace
post_agents(prepped_agents)

