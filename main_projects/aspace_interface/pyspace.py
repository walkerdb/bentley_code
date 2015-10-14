import requests
import json
import os

class PySpace (object):
    def __init__(self, host="http://localhost:8089", username="admin", password="admin", repository="1"):
        self.host = host
        self.repository = repository
        auth_url = "{0}/users/{1}/login?password={2}".format(host, username, password)
        auth_json_response = requests.post(auth_url).json()
        self.session_id = auth_json_response["session"]
        self.headers = {'Content-type': 'application/json', 'X-ArchivesSpace-Session': self.session_id}

    def ead_to_json(self, path_to_ead_file):
        with open(path_to_ead_file, mode="rb") as f:
            headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session': self.session_id}
            request_response = requests.post("{0}/plugins/jsonmodel_from_format/resource/ead".format(self.host), headers=headers, data=f).json()
            if "invalid_object" in request_response:
                print("error converting to json: {0}".format(request_response["error"]))

        return request_response

    def post_ead(self, path_to_ead_file):
        json_data = self.ead_to_json(path_to_ead_file)
        response = requests.post("{0}/repositories/{1}/batch_imports".format(self.host, self.repository), headers=self.headers, data=json.dumps(json_data)).json()
        # print(json_data)
        print(json.dumps(response))

    def post_accession(self, accession_json):
        if type(accession_json) == str:
            accession_json = json.loads(accession_json)
        return requests.post("{0}/repositories/{1}/accessions".format(self.host, self.repository), headers=self.headers, data=json.dumps(accession_json)).json()


    def change_repository(self, repository_number):
        self.repository = repository_number