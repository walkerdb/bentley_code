import codecs
from collections import Counter
import csv
from lxml import etree
import os
import cStringIO
import re
from tqdm import tqdm
from utilities.ead_utilities.ead_utilities import EADDir, EAD


def main():
    results = []
    ead_dir = EADDir()
    for filename in tqdm(ead_dir.ead_files):
        ead = EAD(os.path.join(ead_dir.input_dir, filename))
        results += get_physfacet_texts(ead)

    counts = Counter([result[0] for result in results])

    with open("physfacet_counts.csv", mode="wb") as f:
        writer = UnicodeWriter(f)
        writer.writerow(["physfacet", "count"])
        writer.writerows(sorted(sorted(counts.most_common()), key=lambda x: -x[1]))

    with open("physfacets_with_locations.csv", mode="wb") as f:
        writer = UnicodeWriter(f)
        writer.writerow(["physfacet text", "collection", "filename", "xpath"])
        writer.writerows(sorted(results))


def get_physfacet_texts(ead):
    physfacets = ead.tree.xpath("//physfacet")
    physfacets = remove_physfacets_with_extents(physfacets)

    return [(extract_text(physfacet), ead.title, ead.filename, ead.tree.getpath(physfacet)) for physfacet in physfacets]


def remove_physfacets_with_extents(physfacets):
    filtered = []
    for physfacet in physfacets:
        if physfacet.xpath("../extent"):
            continue
        filtered.append(physfacet)

    return filtered


def extract_text(tag):
    text = etree.tostring(tag)
    tag_regex = re.compile(r"</?.*?>")

    return " ".join(re.sub(tag_regex, "", text).split()).strip()


class UnicodeWriter:
    # from stackoverflow. it is magic.
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        '''writerow(unicode) -> None
        This function takes a Unicode string and encodes it to the output.
        '''
        self.writer.writerow([s.encode("utf-8") if type(s) == unicode else unicode(s).encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == "__main__":
    main()
