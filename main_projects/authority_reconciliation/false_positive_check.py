import csv
import re

from fuzzywuzzy import fuzz


def iterate_through_csv(input_filename, output_filename, type_):

    new_auth_data = []
    with open(input_filename, mode="r") as f:
        reader = csv.reader(f)
        for row in reader:
            original_name, lc_name, lc_address = row
            if lc_name:
                if is_same_entity(original_name, lc_name, type_):
                    new_auth_data.append(row)

    with open(output_filename, mode="wb") as f:
        writer = csv. writer(f)
        writer.writerows(new_auth_data)


def is_same_entity(bentley_term, lc_term, type_):
    if "geogname" in type_:
        similarity = fuzz.token_sort_ratio(bentley_term, lc_term)
        return similarity > 95

    elif "corpname" in type_:
        bentley_term = bentley_term.replace("U.S.", "United States")
        lc_term = lc_term.replace("U.S.", "United States")

        bentley_term = bentley_term.replace("N.Y.", "New York")
        lc_term = lc_term.replace("N.Y.", "New York")

        if "." in bentley_term.strip("."):
            similarity = fuzz.ratio(bentley_term, lc_term)
        else:
            similarity = fuzz.WRatio(bentley_term, lc_term)

        # print("{0}: {1} <--> {2}".format(similarity, original_term, returned_term))
        return similarity >= 90

    elif "persname" in type_:
        bias = 0

        date_regex = r"(\d{4})\-((?:\d{4})?)"
        bentley_dates = re.findall(date_regex, bentley_term)
        lc_dates = re.findall(date_regex, lc_term)

        if len(bentley_dates) > 0 and len(lc_dates) > 0:
            birthdate_bentley, deathdate_bentley = bentley_dates[0]
            birthdate_lc, deathdate_lc = lc_dates[0]

            if birthdate_bentley != birthdate_lc:
                bias -= 100

            if birthdate_bentley == birthdate_lc and deathdate_bentley == deathdate_lc:
                bias += 100

            if birthdate_bentley == birthdate_lc and deathdate_lc and not deathdate_bentley:
                lc_term = lc_term.replace(deathdate_lc, "")
                bias += 25

        similarity = fuzz.token_sort_ratio(bentley_term, lc_term) + bias

        print("{0}: {1} <--> {2}".format(similarity, bentley_term, lc_term))
        return similarity >= 95


if __name__ == "__main__":
    input_filename = "geognames_with_ids.csv"
    output_filename = "geognames_with_ids_verified.csv"
    iterate_through_csv(input_filename=input_filename, output_filename=output_filename, type_="geogname")
