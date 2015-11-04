import gzip
import csv
import sys

csv.field_size_limit(sys.maxsize)

from pprint import pprint

def get_bib_data(row, headers):
    return [row.get(header, "") for header in headers]

def main():

    with gzip.open(r'C:\Users\wboyle\Downloads\hathi_full_20151101.txt.gz', 'rb') as f:

        headers = ["ht identifier", "access", "rights", "ht record number", "enumeration/chronology", "source",
                   "source institution record number", "oclc numbers", "ISBNs", "ISSNs", "LCCNs", "title", "imprint",
                   "rights determination reason code", "date of last update", "is government document", "publication date",
                   "publication place", "language", "bibliographic format"]

        results = []
        result_headers = ["ht identifier", "rights", "oclc numbers", "source institution record number", "title", "enumeration/chronology", "imprint", "publication date", "publication place"]
        reader = csv.DictReader(f, delimiter='\t', fieldnames=headers, quoting=csv.QUOTE_NONE)
        for row in reader:
            if "miu" in row.get("publication place", "") or "University of Michigan" in row.get("imprint", ""):
                results.append(get_bib_data(row, result_headers))

        print(len(results))

        with open("combined_results.csv", mode="wb") as g:
            writer = csv.writer(g)
            writer.writerow(result_headers)
            writer.writerows(results)


if __name__ == "__main__":
    main()
