import csv
import os
from utilities.ead_utilities.ead_utilities import EADDir, EAD


def get_unittitles(ead):
    node = ""
    for c01 in ead.tree.xpath("//c01"):
        if c01.xpath("did/unittitle")[0].text == "Project Records":
            node = c01
            break

    unittitles = []
    for c02 in node.xpath("//c02"):
        text = c02.xpath("did/unittitle")[0].text
        unittitles.append([text,])

    with open("kahnalb Project Records unittitles.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerows(unittitles)

if __name__ == "__main__":
    ead_dir = EADDir()
    ead = EAD(os.path.join(ead_dir.input_dir, "kahnalb.xml"))

    get_unittitles(ead)