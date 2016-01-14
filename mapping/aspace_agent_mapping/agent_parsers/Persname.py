import json

from mapping.aspace_agent_mapping.agent_parsers import parse_persname

class Persname:
    def __init__(self, string, auth_id="", auth_source=""):
        data_dict = parse_persname(string, auth_id, auth_source)
        self.aspace_name_json = self.reduce_dict(data_dict)
        self.aspace_date_json = self.create_aspace_dates(data_dict)

    def get_aspace_json(self):
        if self.aspace_date_json:
            if "begin" in self.aspace_date_json or "end" in self.aspace_date_json:
                return json.dumps({"publish": True, "dates_of_existence": [self.aspace_date_json, ], "names": [self.aspace_name_json, ]})

        return json.dumps({"publish": True, "names": [self.aspace_name_json, ]})

    @staticmethod
    def reduce_dict(data_dict):
        aspace_dict = {}
        keys = [u"primary_name", u"title", u"name_order", u"prefix", u"rest_of_name", u"suffix", u"fuller_form", u"number", u"name_order", u"sort_name_auto_generate", u"source", u"authority_id"]
        for key, value in data_dict.items():
            if key in keys:
                aspace_dict[key] = value

        # for key in keys:
        #     if key not in aspace_dict:
        #         aspace_dict[key] = u""

        return aspace_dict

    @staticmethod
    def create_aspace_dates(data_dict):
        expression = str(data_dict.get("date_string", ""))
        birthdate = str(data_dict.get("birth_date", ""))
        deathdate = str(data_dict.get("death_date", ""))

        if birthdate or deathdate:
            date_type = "single"
            if birthdate and deathdate:
                date_type = "range"

            return {"date_type": date_type, "label": "existence", "expression": expression, "begin": birthdate, "end": deathdate}

        return ""
