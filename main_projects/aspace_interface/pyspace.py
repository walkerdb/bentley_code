import requests
import json

class PySpace (object):
    def __init__(self, host="http://localhost:8089", username="admin", password="admin", repository="2"):
        self.host = host
        self.repository = repository

        auth_url = "{0}/users/{1}/login?password={2}".format(host, username, password)
        auth_json_response = requests.post(auth_url).json()

        self.session_id = auth_json_response["session"]
        self.headers = {'Content-type': 'application/json', 'X-ArchivesSpace-Session': self.session_id}

    def ead_to_json(self, path_to_ead_file):
        with open(path_to_ead_file, mode="rb") as f:
            headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session': self.session_id}

            return requests.post("{0}/plugins/jsonmodel_from_format/resource/ead".format(self.host),
                                 headers=headers,
                                 data=f
                                 ).json()

    def post_ead(self, path_to_ead_file):
        json_data = self.ead_to_json(path_to_ead_file)

        return requests.post("{0}/repositories/{1}/batch_imports".format(self.host, self.repository),
                             headers=self.headers,
                             data=json.dumps(json_data)
                             ).json()

    def post_accession(self, accession_json):
        if type(accession_json) == str:
            accession_json = json.loads(accession_json)

        return requests.post("{0}/repositories/{1}/accessions".format(self.host, self.repository),
                             headers=self.headers,
                             data=json.dumps(accession_json)
                             ).json()

    def get_all_object_ids(self, object_type):
        """
        acceptable object types:
            accessions
            archival_objects
            classification_terms
            classifications
            digital_object_components
            digital_objects
            events
            groups
            resources
        """
        headers = {"X-ArchivesSpace-Session": self.session_id}
        return requests.get('{0}/repositories/{1}/{2}?all_ids=true'.format(self.host, self.repository, object_type),
                            headers=headers
                            ).json()

    def delete_aspace_object(self, object_type, aspace_id):
        headers = {"X-ArchivesSpace-Session": self.session_id}
        return requests.delete('{0}/repositories/{1}/{2}/{3}'.format(self.host, self.repository, object_type, aspace_id),
                               headers=headers
                               ).json()

    def change_repository(self, repository_number):
        self.repository = repository_number
