from collections import Counter
from lxml import etree
import os
from pprint import pprint
import re
from tqdm import tqdm
from utilities.ead_utilities.ead_utilities import EADDir, EAD


def main():
    combined_results = []
    ead_dir = EADDir()
    for filename in tqdm(ead_dir.ead_files):
        ead = EAD(os.path.join(ead_dir.input_dir, filename))
        combined_results += get_suspicious_corpnames(ead)

    pprint(sorted(sorted(Counter(combined_results).most_common(), key=lambda x: x[0]), key=lambda x: -x[1]))



def get_suspicious_corpnames(ead):
    results = []
    corpnames = ead.tree.xpath("//corpname")
    disallowed_keywords = ["&amp", "Inc", "Michigan", "University", "United", "(", "Co.", "Ann Arbor"]

    for corpname in corpnames:
        corpname.tail = ""
        text = extract_text(corpname).strip(",")

        if "," in text and all(word not in text for word in disallowed_keywords):
            results.append(text)

    return results


def extract_text(tag):
    text = etree.tostring(tag)
    tag_regex = re.compile(r"</?.*?>")

    return " ".join(re.sub(tag_regex, "", text).split()).strip()

if __name__ == "__main__":
    main()