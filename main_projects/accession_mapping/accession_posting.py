import json
from pprint import pprint
from tqdm import tqdm
from main_projects.aspace_interface.pyspace import PySpace

conn = PySpace(host="http://141.211.39.87:8089/", repository="3", username="wboyle", password="bentley")

with open("json_data.json", mode="r") as f:
    json_data = json.load(f)

for accession_json in tqdm(json_data):
    response = conn.add_accession(accession_json)
    if "invalid_object" in response:
        pprint(json.dumps(response))
