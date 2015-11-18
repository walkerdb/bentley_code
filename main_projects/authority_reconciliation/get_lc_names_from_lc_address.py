import csv
import time

from tqdm import tqdm

from main_projects.authority_reconciliation.viaf_search import get_lc_heading

with open("found_id_dicts/persname_id_dict.txt", mode="r") as f:
    id_dict = eval(f.read())

for bentley_name, lc_address in tqdm(id_dict.items()):
    try:
        lc_name = get_lc_heading(lc_address)
        # print("{0} --> {1}".format(corpname, lc_name))
        row = [bentley_name, lc_name, lc_address]
        with open("working_csvfiles/persnames_with_unverified_ids.csv", mode="ab") as f:
            csv.writer(f).writerow(row)
    except:
        print("failure at {0}".format(lc_address))
    time.sleep(0.1)
