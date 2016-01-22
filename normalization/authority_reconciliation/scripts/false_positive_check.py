import re

from fuzzywuzzy import fuzz

def filter_out_false_positives(subjects_with_lc_auth_names):
    results = set()

    for subject_tuple in subjects_with_lc_auth_names:
        auth_type, local_term, lc_term, lc_link = subject_tuple

        if not is_same_entity(local_term, lc_term, auth_type):
            continue

        results.add(subject_tuple)

    return results

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

