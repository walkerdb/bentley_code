import csv
import re

from tqdm import tqdm
from fuzzywuzzy import fuzz


def iterate_through_csv(input_filename, output_filename, controlaccess_type):

    new_auth_data = []
    bad_auth_data = []
    with open(input_filename, mode="r") as f:
        reader = csv.reader(f)
        for row in tqdm(list(reader)):
            original_name, lc_name, lc_address = row
            if lc_name:
                if is_same_entity(original_name, lc_name, controlaccess_type):
                    new_auth_data.append(row)
                else:
                    bad_auth_data.append(row)

    with open(output_filename, mode="wb") as f:
        writer = csv.writer(f)
        writer.writerows(sorted(new_auth_data))

    with open("working_csvfiles/{0}_bad_matches.csv".format(controlaccess_type), mode="wb") as f:
        writer = csv.writer(f)
        writer.writerows(sorted(bad_auth_data))


def is_same_entity(local_term, lc_term, controlaccess_type):

    if u"geogname" in controlaccess_type:
        # geognames are a simple check. Returns true if the
        # similarity is > 95; else false
        similarity = fuzz.token_sort_ratio(local_term, lc_term)
        return similarity > 95

    elif u"corpname" in controlaccess_type:
        # replace some common abbreviations with their full forms
        local_term = local_term.replace(u"U.S.", u"United States")
        lc_term = lc_term.replace(u"U.S.", u"United States")

        local_term = local_term.replace(u"N.Y.", u"New York")
        lc_term = lc_term.replace(u"N.Y.", u"New York")

        # custom checks for compound corpnames (separated by a ". ")
        # if it's not a compound name, it does a "WRatio" comparison,
        # which is essentially a kitchen-sink method that does every
        # type of comparison fuzzywuzzy is capable of, and returns the
        # highest resulting value.
        if "." in local_term.strip("."):
            similarity = fuzz.ratio(local_term, lc_term)
        else:
            similarity = fuzz.WRatio(local_term, lc_term)

        return similarity >= 90

    elif u"persname" in controlaccess_type:
        # The persname check performs a normal fuzz comparison,
        # but also explicitly compares birth and death dates,
        # adding a bias to the fuzz score based on those results
        bias = 0

        # regex for extracting birth and death dates
        date_regex = r"(\d{4})\-((?:\d{4})?)"

        # using the regex to grab dates from the local and lc terms
        local_dates = re.findall(date_regex, local_term)
        lc_dates = re.findall(date_regex, lc_term)

        # date comparison code
        # only runs if both the local and lc terms contain dates
        if len(local_dates) > 0 and len(lc_dates) > 0:

            # set local and lc birth and death dates
            birthdate_local, deathdate_local = local_dates[0]
            birthdate_lc, deathdate_lc = lc_dates[0]

            # if birthdates don't match it's definitely the wrong person
            if birthdate_local != birthdate_lc:
                bias -= 100

            # if all the dates match, it's definitely the same person
            if birthdate_local == birthdate_lc and deathdate_local == deathdate_lc:
                bias += 100

            # If the local and lc birthdates match, but the lc has a
            # deathdate and we do not, then it's likely the case that
            # our term just needs to be updated. We'll add a bit of bias
            # and remove the LC death date just for comparison purposes
            if birthdate_local == birthdate_lc and deathdate_lc and not deathdate_local:
                lc_term = lc_term.replace(deathdate_lc, "")
                bias += 25

        # similarity is the fuzz ratio plus the bias calculated above
        similarity = fuzz.token_sort_ratio(local_term, lc_term) + bias

        return similarity >= 95


if __name__ == "__main__":
    types = [u"persname", u"geogname", u"corpname"]
    for controlaccess_type in types:
        input_filename = "working_csvfiles/all_{0}_matches_(unverified).csv".format(controlaccess_type)
        output_filename = "working_csvfiles/{0}s_with_ids_verified.csv".format(controlaccess_type)
        iterate_through_csv(input_filename=input_filename, output_filename=output_filename, controlaccess_type=controlaccess_type)
