from urllib2 import urlopen, quote
import csv
import time

from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm

search_types = ["geographicNames", "personalNames", "corporateNames"]


def main():
    with open("geognames.csv") as f:
        reader = csv.reader(f)
        for location in tqdm(list(reader)):
            if "--" not in location[0]:
                get_auth_id_from_api("viaf", "lc", location[0], search_type="geographicNames")

                time.sleep(.1)


def get_auth_id_from_api(target_api, auth_source, search_term, search_type):
    query = create_query(target_api, auth_source, search_term, search_type)
    response = urlopen(query).read()
    heading, lc_address = _get_auth_data(target_api, response)

    with open("geognames_with_unverified_ids.csv", mode="ab") as f:
        writer = csv.writer(f)
        row = [search_term, heading, lc_address]
        writer.writerow(row)


def _get_auth_data(target_api, response):
    if "viaf" in target_api:
        lc_template = "http://id.loc.gov/authorities/names/{0}.html"
        lc_address = ""
        heading = ""
        tree = etree.fromstring(response)
        results = tree.xpath("//*[local-name()='record']")
        if len(results) > 0:
            primary_result = results[0]
            sources = primary_result.xpath("//*[local-name()='mainHeadingEl']/*[local-name()='id']")
            for source in sources:
                if "LC|" in source.text:
                    lc_address = lc_template.format(source.text.split("|")[1].replace(" ", ""))
                    heading = get_lc_heading(lc_address)
                    break

        return heading, lc_address


def get_lc_heading(lc_address):
    try:
        response = urlopen(lc_address).read()
        soup = BeautifulSoup(response)
        header = soup.h1.text.encode("utf-8")
        return header
    except:
        return "[LC link 404s]"


def create_query(target_api, auth_source, search_term, search_type=""):
    auth_source = quote('"{}"'.format(auth_source))
    search_term = quote('"{}"'.format(search_term))

    if "viaf" in target_api:
        search_url_template = 'http://viaf.org/viaf/search/viaf?query=local.{0}+all+{1}+and+local.sources+any+{2}&sortKeys=holdingscount&httpAccept=application/xml'
        return search_url_template.format(search_type, search_term, auth_source)

    elif "lc" in target_api:
        pass

    elif "aat" in target_api:
        pass

    elif "geonames" in target_api:
        pass


if __name__ == "__main__":
    main()
