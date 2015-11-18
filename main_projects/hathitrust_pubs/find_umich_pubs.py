from collections import defaultdict
import gzip
import csv
from itertools import groupby
from operator import itemgetter
from pprint import pprint
import sys
import json

from natsort import natsort


# TODO add enumeration summary, rights summary, pub dates summary
# enumeration summary should have:
    # volumes present
    # volumes missing

# rights summary would ideally have date ranges associated with them, if there are multiple

# publication date summary


class PrettyDefaultDict(defaultdict):
    __repr__ = dict.__repr__

csv.field_size_limit(sys.maxsize)

def extract_umich_pubs(filepath_to_gz_file):
    with gzip.open(filepath_to_gz_file, 'rb') as f:

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
        identifier = pub.get("oclc numbers", "") or "local (non-oclc): " + pub["source institution record number"]
        enumeration = pub.get("enumeration/chronology", "no enumeration value") or "no enumeration value"
        groups[identifier][enumeration].append(pub)

    return groups

def summarize_digit_list(list_or_set):
    # In some cases there are hundreds of "missing" boxes. To make the output more human-readable, the code below
    # contracts sequential series of missing numbers into a range, e.g. [1, 2, 3, 4] into "1-4"

    # First extract each series of sequential numbers
    # (code from the python docs, see https://docs.python.org/2.6/library/itertools.html#examples)
    range_lists = []
    for k, g in groupby(enumerate(list_or_set), lambda ix: ix[0]-ix[1]):
        range_lists.append(map(itemgetter(1), g))

    # make each sequence human-readable, by grabbing the first and last values of each sequence list
    ranges = []
    for range in range_lists:
        if len(range) > 1:
            ranges.append("{0}-{1}".format(range[0], range[-1]))
        elif len(range) == 1:
            ranges.append(str(range[0]))

    # Since this is a list of strings that sometimes contain non-numeric characters, we use the naturalsort library to
    # return the results in the expected order. Otherwise ["2-10", "11-19", "20"] would be sorted ["11-19", "2-10", "20"]
    return natsort(ranges)


def get_missing_numbers(list_or_set):
    # set the maximum and minimum box numbers found in the given box-number list
    min_number = min(list_or_set)
    max_number = max(list_or_set)

    missing_numbers = []

    # for each integer between the minimum and maximum value, check if that integer is in the box list.
    # If it does not, that box is missing.
    i = min_number
    while i < max_number:
        if i not in list_or_set:
            missing_numbers.append(i)
        i += 1

    # sort the list of missing numbers
    missing_numbers.sort()

    return summarize_digit_list(missing_numbers)


def humanize_list(list_or_set):
    list_len = len(list_or_set)

    if list_len == 0:
        return ""

    if list_len == 1:
        return list_or_set[0]

    if list_len == 2:
        return "{} and {}".format(list_or_set[0], list_or_set[1])

    string = ""
    for i, element in enumerate(list_or_set):
        if i == list_len - 1:
            string += "and {}".format(element)
        else:
            string += "{}, ".format(element)

    return string


if __name__ == "__main__":
    # pubs, pub_headers = extract_umich_pubs(r'C:\Users\wboyle\Downloads\hathi_full_20151101.txt.gz')
    #
    # with open("all_results.csv", mode="wb") as g:
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
    headers = ["num_of_items", "oclc identifier", "source institution identifier", "source institution", "title", "imprint", "copyright statuses of publications in series", "publication date range", "earliest publication", "latest publication", "all publication dates"]
    for oclc_identifier, pubs_dict in series.items():
        title = "[no title]"
        contributor = "[none]"
        local_identifier = "[none]"
        imprint = "[none]"
        if not oclc_identifier:
            oclc_identifier = "[none]"

        # since we're only summarizing, we'll just grab info for the first pub in each series
        for volume, pub in pubs_dict.items():
            title = pub[0].get("title", "[no title]")
            contributor = pub[0].get("ht identifier", "[none].none").split(".")[0]
            local_identifier = pub[0].get("source institution record number", "[none]")
            imprint = pub[0].get("imprint", "[none]")
            break

        years = set()
        copyrights = set()
        enumerations = set()
        if "9999" in years:
            years.remove("9999")

        for volume, pubs in pubs_dict.items():
            for pub in pubs:
                year = pub.get("publication date", "")
                if year and year != "9999":
                    years.add(int(year))

                if pub.get("rights", ""):
                    copyrights.add(pub.get("rights", ""))
                if pub.get("enumeration/chronology", ""):
                    enumerations.add(pub.get("enumeration/chronology", ""))
            pass

        humanized_years = "no years in series"
        earliest_year = "no years in series"
        latest_year = "no years in series"
        total_pub_range = "no years in series"
        if years:
            humanized_years = humanize_list(summarize_digit_list(sorted(list(years))))
            earliest_year = min(years)
            latest_year = max(years)
            total_pub_range = "{}-{}".format(earliest_year, latest_year)
        # print(sorted(list(copyrights)))
        # if enumerations:
        #     print(sorted(list(enumerations)))
        # print()

        output.append([len(pubs_dict), oclc_identifier, local_identifier, contributor, title, imprint, humanize_list(sorted(list(copyrights))), total_pub_range, earliest_year, latest_year, humanized_years])

    with open("summary.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(output)
