'''
Tool to find any word doc finding-aids that may contain more recent information than our EAD files.
'''

import os
import csv
from datetime import datetime


def main():
    ead_dir = r"C:\Users\wboyle\PycharmProjects\bentley_code\Original EADs"
    doc_dir = r"C:\Users\wboyle\PycharmProjects\bentley_code\Original Docs"
    with open("docs_that_are_newer_than_eads.csv", mode="wb") as f:
        writer = csv.writer(f)
        header = ["filename", "Doc last modified date", "EAD last modified date", "difference in days"]
        writer.writerow(header)

    date_dict = {}
    for ead in os.listdir(ead_dir):
        if ead.endswith(".xml"):
            time = os.path.getmtime(os.path.join(ead_dir, ead))
            time = datetime.fromtimestamp(time)
            name_without_extension = ead.split(".")[0]
            date_dict[name_without_extension] = time

    total = 0
    for doc in os.listdir(doc_dir):
        if doc.endswith(".doc") or doc.endswith(".docx"):
            time = os.path.getmtime(os.path.join(doc_dir, doc))
            time = datetime.fromtimestamp(time)
            name_without_extension = doc.split(".")[0]

            if name_without_extension in date_dict:
                if time > date_dict[name_without_extension]:
                    delta = time - date_dict[name_without_extension]
                    if delta.days == 46:
                        continue
                    if delta.seconds > 1800:
                        print("\n{0} > {1}".format(time, date_dict[name_without_extension]))
                        print("{} is newer than its ead!\n".format(name_without_extension))
                        total += 1
                        with open("docs_that_are_newer_than_eads.csv", mode="ab") as f:
                            days = delta.days
                            print(days)
                            writer = csv.writer(f)
                            row = [name_without_extension, time, date_dict[name_without_extension], days]
                            writer.writerow(row)
                    else:
                        print("{} is just slightly newer than its ead.".format(name_without_extension))
            else:
                # print("{} seems to have no EAD analog".format(name_without_extension))
                pass
    print(total)






if __name__ == "__main__":
    main()

