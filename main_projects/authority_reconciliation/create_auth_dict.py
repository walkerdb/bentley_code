import csv
from pprint import pprint

def create_auth_dict(input_file, output_filename):
    auth_dict = {}
    with open(input_file, mode="r") as f:
        reader = csv.reader(f)
        for row in reader:
            original_name, lc_name, lc_address = row
            auth_dict[original_name] = [lc_name, lc_address]

    with open(output_filename, mode="w") as f:
        pprint(auth_dict, stream=f)

if __name__ == "__main__":
    types = ["persname", "geogname", "corpname"]
    for type_ in types:
        input_file = "working_csvfiles/{0}s_with_verified_ids.csv".format(type_)
        output_file = "found_id_dicts/{0}_id_dict.txt".format(type_)
        create_auth_dict(input_file=input_file, output_filename=output_file)
