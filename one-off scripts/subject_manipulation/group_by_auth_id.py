from collections import defaultdict
import csv
from pprint import pprint


def get_data(filename):
    with open(filename, mode="rb") as f:
        data = []
        reader = csv.DictReader(f)
        for dct in reader:
            data.append(dct)

    return data


def group_by_id(dct_list):
    data = defaultdict(set)
    for dct in dct_list:
        id = dct["auth id"]
        if not id:
            continue

        data[id].add((dct["type"], dct["text"]))

    return {k: v for k, v in data.items() if len(v) > 1}


if __name__ == "__main__":
    data = group_by_id(get_data("all_subjects_new.csv"))
    with open("auth_id_things.txt", mode="w") as f:
        pprint(data.values(), stream=f, width=90)

    with open("multiple_values_same_auth_id.csv", mode="wb") as f:
        output = []
        for k, v in data.items():
            row = [k]
            for tup in v:
                row.append("{}: {}".format(tup[0], tup[1]))
            for i in range(5 - len(row)):
                row.append("")
            output.append(row)

        headers = ["auth id", "tag 1", "tag 2", "tag 3", "tag 4"]

        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(output)
