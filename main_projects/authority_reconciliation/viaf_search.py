from urllib2 import urlopen, quote
import httplib
from collections import namedtuple

search_url_template = 'http://viaf.org/viaf/search/viaf?query=local.{0}+all+{1}+and+local.sources+any+{2}&sortKeys=holdingscount&httpAccept=application/xml'

SearchTypes = namedtuple("SearchTypes", ["geogname", "corpname", "persname"])
search_types = SearchTypes(
	geogname="geographicNames",
	persname="personalNames",
	corpname="corporateNames"
)

authority_source = quote('"lc"')
search_term = quote('"Zeeland (Mich.)"')
query = search_url_template.format(search_types.geogname, search_term, authority_source)
print(query)

data = urlopen(query)

print(data.read())
