import json

from mapping.aspace_agent_mapping.agent_parsers import parse_famname

class Famname:
    def __init__(self, string, auth_id="", auth_source=""):
        self.data_dict = parse_famname(string, auth_id, auth_source)

    def get_aspace_json(self):
        return json.dumps({"publish": True, "names": [self.data_dict]})
