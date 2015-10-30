import csv
import json
import re
from tqdm import tqdm


def make_accession_json_list(filepath):
    all_json_data = []

    deaccessions_or_disposition_fields = ["Description", "DestructionDate", "Location", "ReturnDate",
                                          "SeparationsType", "Volume"]

    digital_extent_fields = ["DigitalSize", "DigitalSizeType"]

    user_defined_field_mappings = {"Acknowledged": "boolean_1",
                           "StaffReceived": "string_1",
                           "ThankYouNote": "text_1",
                           "GiftAgreementStatus": "enum_1",
                           "LocationInfo": "text_2"}

    collection_management_mappings = {"Difficulty": "processing_plan",
                                      "PercentageToRetain": "processing_plan",
                                      "ProcessNote": "processing_plan",
                                      "PriorityLevel": "processing_priority",
                                      "Processor": "processors"}

    external_documents_fields = ["FileLink"]

    access_restriction_fields = ["RestrictionsType", "Note"]

    simple_field_mappings = {'AccDescription': 'content_description',
                             'AccessionDate': 'accession_date',
                             'AccessionID': 'id_0',
                             'DonorBoxList': 'inventory',
                             'GivenThrough': 'provenance',
                             "DonorType": "acquisition_type",
                             "MHCType": "resource_type",
                             "Notes": "use_restrictions_note"}

    accession_dicts = get_accessions(filepath)
    for accession in tqdm(accession_dicts):
        json_data = {}

        # make the simple plain-text fields
        for accession_key, json_key in simple_field_mappings.items():
            text = ""
            if accession.get(accession_key, ""):
                text = accession.get(accession_key, "").strip()
            if text:
                if accession_key == "AccessionDate":
                    text = make_date_text(text)

                elif accession_key == "DonorType":
                    if "purchase" in text.lower():
                        text = "purchase"
                    else:
                        text = "deposit"

                elif accession_key == "MHCType":
                    if "published" in text.lower():
                        text = "publications"
                    else:
                        text = "papers"

                json_data[json_key] = text

        if accession.get('AccDescription', "").strip():
            json_data["title"] = accession.get('AccDescription', "").strip()
        # now make the fields that consist of ASpace objects

        # disposition or deaccession
        deaccessions = []
        if is_disposition(accession):
            json_data["disposition"] = make_disposition_text(accession)
        else:
            deaccessions.append(make_deaccession_json(accession))
        # hack of a fix to get rid of empty dispositions
        if "disposition" in json_data and not json_data.get("disposition", ""):
            del json_data["disposition"]
        if len(deaccessions) > 0:
            json_data["deaccessions"] = deaccessions

        # things going in user defined fields
        user_defined_data = make_user_defined_json(accession, user_defined_field_mappings)
        if user_defined_data:
            json_data["user_defined"] = user_defined_data

        # extents
        extents = []
        if accession.get("DigitalSize", "").strip():
            type_ = accession.get("DigitalSizeType", "")
            if type_ in ["MB", "GB", "KB", "TB"]:
                extents.append(make_extent_json(
                    number=accession.get("DigitalSize", ""),
                    type_=accession.get("DigitalSizeType", "(MB?)"))
                )

        if accession.get("LinearFeet", "").strip():
            extents.append(make_extent_json(number=accession.get("LinearFeet", "")))

        json_data["extents"] = extents

        # collection management
        if any([accession.get(field, "").strip() for field in collection_management_mappings.keys()]):
            json_data["collection_management"] = make_collection_management_json(accession, collection_management_mappings)

        # external documents
        external_documents = []
        for doc_field in external_documents_fields:
            if accession.get(doc_field, ""):
                external_documents.append(make_external_document_json(accession.get(doc_field), doc_type=doc_field))

        # access restrictions
        if any([accession.get(field, "").strip() for field in access_restriction_fields]):
            json_data["access_restrictions_note"] = "Restriction type: {}\nRestriction note: {}".format(accession.get("RestrictionsType", ""), accession.get("Notes", ""))

        all_json_data.append(json_data)

    return all_json_data


def get_accessions(filepath):
    with open(filepath, mode="r") as f:
        reader = csv.DictReader(f)
        accessions = [row for row in reader]

    return accessions


def is_disposition(accession):
    return not accession.get("DestructionDate", "") and not accession.get("ReturnDate", "")


def make_date_text(text):
    regex = re.compile(r"/|\.|\-")
    parts = re.split(regex, text)
    try:
        parts = [int(part) for part in parts]
        if len(parts) == 2:
            month, year = parts
            day = 1
            print(text)
        elif len(parts) == 3:
            month, day, year = parts
        elif len(parts) == 1:
            year = parts[0]
            month = 1
            day = 1
            print(text)
        else:
            print(text)
            year, month, day = (1800, 1, 1)
    except ValueError:
        print(text)
        year, month, day = (1800, 1, 1)

    return "{:04d}-{:02d}-{:02d}".format(year, month, day)


def make_disposition_text(accession):
    description = accession.get("Description", "")
    location = accession.get("Location", "")
    type_ = accession.get("SeparationsType", "")
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

    return text.strip()


def make_collection_management_json(accession, fields):
    d = {}

    processing_plan_string = ""
    for accession_key in [key for key, value in fields.items() if value == "processing_plan"]:
        if accession.get(accession_key, ""):
            processing_plan_string += "{}: {}\n".format(accession_key, accession[accession_key])

    if processing_plan_string:
        d["processing_plan"] = processing_plan_string

    for accession_key, json_key in [(key, value) for key, value in fields.items() if value != "processing_plan"]:
        if accession.get(accession_key, ""):
            if json_key == "processing_priority":
                value = accession[accession_key].lower()
                if value in ["high", "low", "medium"]:
                    d[json_key] = value
            else:
                d[json_key] = accession[accession_key]

    return d


def make_deaccession_json(accession):
    d = {"extents": []}

    destruction_date = accession.get("DestructionDate", "")
    return_date = accession.get("ReturnDate", "")
    volume = accession.get("Volume", "")

    d["description"] = accession.get("Description", "Deaccession not described")
    if not d["description"]:
        d["description"] = "Deaccession not described"
    d["scope"] = "part"

    # TODO deaccession objects can only take one date, BUT some accession records have both returned and destroyed dates.
    # do something about that.
    if destruction_date.strip():
        d["date"] = make_date_json(
            type_="single",
            label="deaccession",
            expression="Material destroyed on " + destruction_date,
            begin_date=make_date_text(destruction_date)
        )

    if return_date.strip():
        d["date"] = make_date_json(
            type_="single",
            label="deaccession",
            expression="Returned to donor on " + return_date,
            begin_date=make_date_text(return_date)
        )

    if volume.strip():
        d["extents"].append(make_extent_json(number=volume))

    return d


def make_date_json(type_, label, expression="", begin_date="", end_date=""):
    return {"date_type": type_, "label": label, 'expression': expression, "begin": begin_date, "end": end_date}


def make_external_document_json(text, doc_type='File Link'):
    return {'location': text, 'title': doc_type}


def make_extent_json(number, type_='linear feet', portion='whole'):
    return {'number': number, 'extent_type': type_, 'portion': portion}


def make_user_defined_json(accession, field_mappings):
    d = {}
    for accession_key, json_key in field_mappings.items():
        text = ""
        if accession.get(accession_key, ""):
            text = accession.get(accession_key, "").strip()
        if text:
            text = text.replace(";;;", "\n")
            if json_key.startswith("boolean"):
                try:
                    text = bool(int(text))
                except:
                    text = False
            elif json_key == ("enum_1"):
                text = text.lower()
                if "file" in text.lower() and "on" in text.lower():
                    text = "on file"
                if "to be sent" in text.lower():
                    text = "pending"

            d[json_key] = text

    return d


if __name__ == "__main__":
    json_data = make_accession_json_list(r"C:\Users\wboyle\PycharmProjects\bentley_code\main_projects\accession_mapping\accessions_20151030-final.csv")
    with open("json_data.json", mode="w") as f:
        f.write(json.dumps(json_data, indent=4, sort_keys=True, ensure_ascii=False))

