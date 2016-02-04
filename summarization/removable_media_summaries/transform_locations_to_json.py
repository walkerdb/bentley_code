import csv
import json


def extract_location_data(row):
    new_row = dict(row)
    # if new_row["box start"]:
    #     new_row["box start"] = int(new_row["box start"])
    # if new_row["box end"]:
    #     new_row["box end"] = int(new_row["box end"])
    del new_row["ID"]
    del new_row["collection title"]
    del new_row["access restrictions"]
    return [new_row, ]


with open("location_export.csv", mode="r") as f:
    data_by_id = {}
    reader = csv.DictReader(f)

    location_data = []
    last_key = "dummy"
    last_data = {}
    for row in reader:
        if row["ID"]:
            data_by_id[last_key] = last_data

            last_key = row["ID"]
            last_data = {"collection title": row["collection title"],
                         "access restrictions": row["access restrictions"],
                         "locations": extract_location_data(row)}
        else:
            last_data["locations"].append(extract_location_data(row))

    with open("locations.json", mode="w") as f:
        json.dump(data_by_id, f, sort_keys=True, indent=4)