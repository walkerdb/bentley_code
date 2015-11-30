from main_projects.aspace_agent_mapping.parsers.create_famname_json import parse_famname

class Famname:
    def __init__(self, string, auth_id="", auth_source=""):
        self.data_dict = parse_famname(string, auth_id, auth_source)

    def get_aspace_json(self):
        return {"publish": True, "agent_type": "agent_family", "names": [self.data_dict]}
