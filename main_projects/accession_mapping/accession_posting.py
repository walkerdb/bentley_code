import json
from pprint import pprint
from main_projects.aspace_interface.pyspace import PySpace


conn = PySpace()

with open("json_data.json", mode="r") as f:
    json_data = json.load(f)

for accession_json in json_data:
    response = conn.post_accession(accession_json)
    if "invalid_object" in response:
        pprint(json.dumps(response))
