from bs4 import BeautifulSoup

import re

def main():

    with open("output2.html", mode="r") as f:
        soup = BeautifulSoup(f.read())

    elements = soup("div", class_="event-description")

    for element in elements:


    with open("output3.html", mode="w") as f:
        f.write(etree.tostring(full_html, pretty_print=True))

    # TODO - manually write out what I'm looking for to an HTML file

    print()


def extract_year(string):

    regex = re.compile(r"19\d\d")
    year = re.findall(regex, string)
    if year:
        year = year[0]
    else:
        year = ""
    return year

if __name__ == "__main__":
    main()