from collections import defaultdict
import csv
import gzip
from itertools import groupby
import json
from operator import itemgetter
import os
from natsort import natsort

__author__ = 'wboyle'

class HTPubSummarizer:
    def __init__(self, source_file):
        # these headers must stay in this order - this is the order they are in in the original HT data file
        self.all_hathitrust_headers = ["ht identifier", "access", "rights", "ht record number",
                                       "enumeration/chronology", "source", "source institution record number",
                                       "oclc numbers", "ISBNs", "ISSNs", "LCCNs", "title", "imprint",
                                       "rights determination reason code", "date of last update",
                                       "is government document", "publication date", "publication place", "language",
                                       "bibliographic format"]

        self.data_to_extract = ["ht identifier", "rights", "oclc numbers", "source institution record number", "title",
                               "enumeration/chronology", "imprint", "publication date", "publication place"]

        self.data = self._load_data(source_file)

        # a dictionary in the form
        # {oclc_identifier, publications_with_that_identifier{
        #                       volume_number, publication_dict{
        #                              publication data faceted by data_to_extract}
        #                       }
        # }
        self.grouped_data = self._group_data_by_id_numbers()


    def summarize(self):
        output = []
        headers = ["num_of_items", "oclc identifier", "source institution identifier", "source institution", "title",
                   "imprint", "copyright statuses of publications in series", "publication date range",
                   "earliest publication", "latest publication", "all publication dates"]

        for oclc_identifier, pubs_dict in self.grouped_data.items():
            data_dict = self._initialize_series_dict(oclc_identifier)

            data_dict.update(self._extract_full_series_metadata(pubs_dict))
            data_dict.update(self._extract_series_item_metadata(pubs_dict))

            data_dict.update(self._summarize_years(data_dict))
            data_dict.update(self._summarize_copyrights(data_dict))
            data_dict.update(self._summarize_enumerations(data_dict))

            row = self._make_output_row(data_dict, headers)

            output.append(row)


        with open("summary.csv", mode="wb") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(output)


    def _summarize_years(self, data_dict):
        d = {}
        if data_dict["years"]:
            d["humanized_years"] = self._humanize_list(self._summarize_digit_list(sorted(list(data_dict["years"]))))
            d["earliest_year"] = min(data_dict["years"])
            d["latest_year"] = max(data_dict["years"])
            d["total_pub_range"] = "{}-{}".format(data_dict["earliest_year"], data_dict["latest_year"])

        return d


    def _summarize_copyrights(self, data_dict):
        return {"copyright_statuses": self._humanize_list(data_dict["copyrights"])}


    def _summarize_enumerations(self, data_dict):
        # TODO - implement something here
        return {}


    @staticmethod
    def _make_output_row(data_dict, headers):
        return [data_dict[header] for header in headers]

    @staticmethod
    def _extract_full_series_metadata(pubs_dict):
        d = {"num_of_items": len(pubs_dict)}

        # since we're only summarizing, we'll just grab info for the first pub in each series
        for volume, pub in pubs_dict.items():
            d["title"] = pub[0].get("title", "[no title]")
            d["contributor"] = pub[0].get("ht identifier", "[none].none").split(".")[0]
            d["local_identifier"] = pub[0].get("source institution record number", "[none]")
            d["imprint"] = pub[0].get("imprint", "[none]")
            break

        return d

    @staticmethod
    def _extract_series_item_metadata(pubs_dict):
        d = {"years": set(), "copyrights": set(), "enumerations": set()}

        for volume, pubs in pubs_dict.items():
            for pub in pubs:
                year = pub.get("publication date", "")
                if year and year != "9999":
                    d["years"].add(int(year))

                if pub.get("rights", ""):
                    d["copyrights"].add(pub.get("rights", ""))

                if pub.get("enumeration/chronology", ""):
                    d["enumerations"].add(pub.get("enumeration/chronology", ""))

        return d


    @staticmethod
    def _initialize_series_dict(oclc_identifier):
        return {"title": "[no title]",
                "contributor": "[none]",
                "local_identifier": "[none]",
                "imprint": "[none]",
                "oclc_identifier": oclc_identifier if oclc_identifier else "[none]",
                "years": set(),
                "copyrights": set(),
                "copyright_statuses": "no copyrights",
                "enumerations": set(),
                "humanized_years": "no years in series",
                "earliest_year": "no years in series",
                "latest_year": "no years in series",
                "total_pub_range": "no years in series"}


    def _load_data(self, source_file):
        filename, extension = os.path.splitext(source_file)
        if extension == ".json":
            return self._load_data_from_json(source_file)
        elif extension == ".gz":
            return self._load_data_from_ht_gzip_dump(source_file)
        else:
            return []


    def _load_data_from_ht_gzip_dump(self, path_to_gz_file):
        with gzip.open(path_to_gz_file, mode='rb') as f:
            reader = csv.DictReader(f, delimiter="\t", fieldnames=self.all_hathitrust_headers, quoting=csv.QUOTE_NONE)
            return self._facet_by_umich_publisher(reader)


    def _facet_by_umich_publisher(self, reader):
        results = []
        for row in reader:
            if "University of Michigan" not in row.get("imprint", ""):
                continue
            results.append(self._extract_relevant_rows(row))

        return results


    def _extract_relevant_rows(self, row):
        return {key: value for (key, value) in row.items() if key in self.data_to_extract}


    def _group_data_by_id_numbers(self):
        grouped_data = defaultdict(lambda: defaultdict(list))
        for pub in self.data:
            identifier = pub.get("oclc numbers", "") or "local (non-oclc): " + pub["source institution record number"]
            enumeration = pub.get("enumeration/chronology", "no enumeration value") or "no enumeration value"
            grouped_data[identifier][enumeration].append(pub)
        return grouped_data


    @staticmethod
    def _load_data_from_json(path_to_json):
        with open(path_to_json, mode="r") as f:
            return json.load(f)


    @staticmethod
    def _humanize_list(list_or_set):
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


    @staticmethod
    def _summarize_digit_list(list_or_set):
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


    @staticmethod
    def _write_data_to_json(filename, json_data):
        with open(filename, mode="w") as f:
            f.write(json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False, encoding="utf-8"))

