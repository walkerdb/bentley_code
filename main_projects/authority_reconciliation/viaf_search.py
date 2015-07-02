from urllib2 import urlopen, quote
import csv
import time

search_types = ["geographicNames", "personalNames", "corporateNames"]


def get_auth_id_from_api(target_api, auth_source, search_term, search_type):
	query = create_query(target_api, auth_source, search_term, search_type)
	print(query)
	response = urlopen(query).read()
	print(response)


def create_query(target_api, auth_source, search_term, search_type=""):
	auth_source = quote('"{}"'.format(auth_source))
	search_term = quote('"{}"'.format(search_term))

	if "viaf" in target_api:
		search_url_template = 'http://viaf.org/viaf/search/viaf?query=local.{0}+all+{1}+and+local.sources+any+{2}&sortKeys=holdingscount&httpAccept=application/xml'

		return search_url_template.format(search_type, search_term, auth_source)

	elif "lc" in target_api:
		pass

	# add more API cases here

if __name__ == "__main__":
	with open("geognames.csv") as f:
		reader = csv.reader(f)
		for location in reader:
			get_auth_id_from_api("viaf", "lc", location[0], search_type="geographicNames")

			time.sleep(2)