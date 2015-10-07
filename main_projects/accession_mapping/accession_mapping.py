import csv
from collections import OrderedDict

def main():
    filepath = ""
    all_json_data = []

    deaccessions_or_disposition_fields = ["Description", "DestructionDate", "Location", "ReturnDate", "Type (AQ)", "Volume", "LinearFeet"]
    digital_extent_fields = ["DigitalSize", "DigitalType"]

    #TODO fix this once Dallas modifies the cleanup code
    user_defined_fields = [("Acknowledged", "boolean_1"),
                           ("StaffReceived", "string_1"),
                           ("ThankYouNote", "text_1"),
                           ("Status (AD)", "enum_1"),
                           ("something to do with the unprocessed location fields", "")]

    collection_management_fields = ["Difficulty", "PercentageToRetain", "ProcessNote", "PriorityLevel", "Processor"]

    external_documents_fields = ["FileLink"]

    access_restriction_fields = ["Type", "Note (AK)"]

    simple_field_mappings = {'AccDescription': 'content_description',
                             'AccessionDate': 'accession_date',
                             'AccessionID': 'id_0',
                             'DonorBoxList': 'inventory',
                             'GivenThrough': 'provenance',
                             "DonorType": "acquisition_type",
                             "MHCType": "resource_type",
                             "Notes (AC)": "use_restrictions_note"}

    accession_dicts = get_accessions(filepath)
    for accession in accession_dicts:
        json_data = {}

        # make the simple plain-text fields
        for accession_key, json_key in simple_field_mappings.items():
            json_data[json_key] = accession.get(accession_key, "")

        # now make the fields that consist of ASpace objects

        # disposition or deaccession
        if is_disposition(accession):
            json_data["disposition"] = make_disposition_text(accession)
        else:
            json_data["deaccessions"] = make_deaccession_json(accession)


def get_accessions(filepath):
    with open(filepath, mode="r") as f:
        reader = csv.DictReader(f)
        accessions = [row for row in reader]

    return accessions


def is_disposition(accession):
    return not accession.get("DestructionDate") and not accession.get("ReturnDate")


def make_disposition_text(accession):
    description = accession.get("Description", "")
    location = accession.get("Location", "")
    type_ = accession.get("Type (AQ)", "")
    volume = accession.get("Volume", "")

    text = ""
    if description:
        text += "Description: {}\n".format(description)
    if location:
        text += "Location: {}\n".format(location)
    if type_:
        text += "Type: {}\n".format(type_)
    if volume:
        text += "Volume: {}\n".format(type_)

    return text


def make_deaccession_json(accession):
    d = {"extents": []}

    destruction_date = accession.get("DestructionDate", "")
    return_date = accession.get("ReturnDate", "")
    volume = accession.get("Volume", "")
    lin_feet = accession.get("LinearFeet")

    d["description"] = accession.get("Description", "")

    # TODO deaccession objects can only take one date, BUT some accession records have both returned and destroyed dates.
    # do something about that.
    if destruction_date:
        d["date"].append(make_date_json(
            type_="Single",
            expression="Material destroyed on " + destruction_date,
            begin_date=destruction_date
        ))

    if return_date:
        d["date"].append(make_date_json(
            type_="Single",
            expression="Returned to donor on " + return_date,
            begin_date=return_date
        ))

    if volume:
        # TODO make the extent bits
        pass


def make_date_json(type_="", expression="", begin_date="", end_date=""):
    return {"type": type_, 'expression': expression, "begin": begin_date, "end": end_date}


def add_extent_type(type_, extent_dict):
    extent_dict['type'] = type_
    return extent_dict


def add_extent_number(number, extent_dict):
    extent_dict['number'] = number
    return extent_dict


def make_external_document_json(text, doc_type='File Link'):
    return {'location': text, 'title': doc_type}


def make_extent_json(number, type_='linear feet', portion='Whole'):
    return {'number': number, 'type': type_, 'portion': portion}


def make_user_defined_field_json(text, type_):
    return{type_: text}
