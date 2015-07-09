import csv
import re

from fuzzywuzzy import fuzz


def iterate_through_csv(input_filename, output_filename, type):

    new_auth_data = []
    with open(input_filename, mode="r") as f:
        reader = csv.reader(f)
        for row in reader:
            original_name, lc_name, lc_address = row
            if lc_name:
                if is_same_entity(original_name, lc_name, type):
                    new_auth_data.append(row)

    with open(output_filename, mode="wb") as f:
        writer = csv. writer(f)
        writer.writerows(new_auth_data)


def is_same_entity(original_term, returned_term, type):
    if "geogname" in type:
        similarity = fuzz.token_sort_ratio(original_term, returned_term)
        return similarity > 95

    elif "corpname" in type:
        original_term = original_term.replace("U.S.", "United States")
        returned_term = returned_term.replace("U.S.", "United States")

        original_term = original_term.replace("N.Y.", "New York")
        returned_term = returned_term.replace("N.Y.", "New York")

        if "." in original_term.strip("."):
            similarity = fuzz.ratio(original_term, returned_term)
        else:
            similarity = fuzz.WRatio(original_term, returned_term)

        print("{0}: {1} <--> {2}".format(similarity, original_term, returned_term))
        return similarity >= 90


if __name__ == "__main__":
    input_filename = "geognames_with_ids.csv"
    output_filename = "geognames_with_ids_verified.csv"
    iterate_through_csv(input_filename=input_filename, output_filename=output_filename, type="geogname")
