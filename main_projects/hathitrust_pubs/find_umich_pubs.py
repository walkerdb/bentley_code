from collections import defaultdict
import gzip
import csv
from pprint import pprint
import sys
import json

class PrettyDefaultDict(defaultdict):
    __repr__ = dict.__repr__

csv.field_size_limit(sys.maxsize)

def extract_umich_pubs():
    with gzip.open(r'C:\Users\wboyle\Downloads\hathi_full_20151101.txt.gz', 'rb') as f:

        headers = ["ht identifier", "access", "rights", "ht record number", "enumeration/chronology", "source",
                   "source institution record number", "oclc numbers", "ISBNs", "ISSNs", "LCCNs", "title", "imprint",
                   "rights determination reason code", "date of last update", "is government document", "publication date",
                   "publication place", "language", "bibliographic format"]

        results = []
        result_headers = ["ht identifier", "rights", "oclc numbers", "source institution record number", "title",
                          "enumeration/chronology", "imprint", "publication date", "publication place"]
        reader = csv.DictReader(f, delimiter='\t', fieldnames=headers, quoting=csv.QUOTE_NONE)
        for row in reader:
            if "University of Michigan" in row.get("imprint", ""):
                results.append(get_relevant_data(row, result_headers))

        print(len(results))

        return results, result_headers


def get_relevant_data(row, headers):
    return [row.get(header, "") for header in headers]


def make_lists_into_dicts(list_of_lists, headers):
    return [{key: value for (key, value) in zip(headers, lst)} for lst in list_of_lists]


def group_by_series(pubs):
    groups = PrettyDefaultDict(lambda: PrettyDefaultDict(list))
    for pub in pubs:
        identifier = pub["source institution record number"]
        enumeration = pub.get("enumeration/chronology", "no enumeration value") or "no enumeration value"
        groups[identifier][enumeration].append(pub)

    return groups


if __name__ == "__main__":
    # pubs, pub_headers = extract_umich_pubs()
    #
    # with open("combined_results.csv", mode="wb") as g:
    #     writer = csv.writer(g)
    #     writer.writerow(pub_headers)
    #     writer.writerows(pubs)

    with open("combined_results.csv", mode="rb") as g:
        pubs = list(csv.reader(g))
        pub_headers = pubs.pop(0)

    # currently a list of lists; make a list of dicts for easier manipulation
    pubs = make_lists_into_dicts(pubs, pub_headers)

    # group publications by their respective series
    series = group_by_series(pubs)
    print(len(series))

    # write those results to a json file
    with open("output.json", mode="w") as f:
        json.dump(series, f, sort_keys=True, indent=4)

    # summarize and write
    output = []
    headers = ["oclc identifier", "source institution identifier", "title", "num_of_items", "source institution"]
    for source_identifier, pubs_dict in series.items():
        title = "[no title]"
        contributor = "[none]"
        oclc_identifier = "[none]"
        if not source_identifier:
            source_identifier = "[none]"

        for volume, pub in pubs_dict.items():
            title = pub[0].get("title", "[no title]")
            contributor = pub[0].get("ht identifier", "[none].none").split(".")[0]
            oclc_identifier = pub[0].get("oclc numbers", "[none]")
        output.append([oclc_identifier, source_identifier, title, len(pubs_dict), contributor])

    with open("summary.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(output)
