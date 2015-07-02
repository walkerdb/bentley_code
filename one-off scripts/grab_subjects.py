from lxml import etree
import csv
import os
from os.path import join

path = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
tags = ['subject', 'corpname', 'geogname', 'persname', 'genreform', 'famname']

def build_master_subject_csv():
	for filename in [ead for ead in os.listdir(path) if ead.endswith(".xml")]:
		print ("working on {0}...".format(filename))
		tree = etree.parse(join(path, filename))

		for controlaccess_child in tree.xpath('//controlaccess/*'):
			if any([controlaccess_child.tag in tag for tag in tags]):

				with open('all_subjects.csv', 'ab') as csvfile:
					writer = csv.writer(csvfile, dialect='excel')

					if controlaccess_child.text is not None and 'source' in controlaccess_child.attrib:
						writer.writerow([filename, controlaccess_child.tag, controlaccess_child.text.encode("utf-8"), controlaccess_child.attrib['source'], tree.getpath(controlaccess_child)])
					elif controlaccess_child.text is not None:
						writer.writerow([filename, controlaccess_child.tag, controlaccess_child.text.encode("utf-8"), '', tree.getpath(controlaccess_child)])
					else:
						continue


def write_unique_subjects_by_tag_to_file():
	subject_count_dict = {}
	for filename in [ead for ead in os.listdir(path) if ead.endswith(".xml")]:
		print ("working on {0}...".format(filename))
		tree = etree.parse(join(path, filename))

		for controlaccess_child in tree.xpath('//controlaccess/*'):
			if any([controlaccess_child.tag in tag for tag in tags]) and controlaccess_child.text is not None:
				text = controlaccess_child.text.encode("utf-8")
				tag = controlaccess_child.tag
				key = "{0}__{1}".format(text, tag)

				subject_count_dict[key] = subject_count_dict.get(key, 0) + 1

	with open('unique_subjects.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile)
		split_data = [[key.split("__")[0], key.split("__")[1], count] for key, count in subject_count_dict.items()]
		subjects = sorted([[tag, subject.rstrip(".").strip()] for subject, tag, count in split_data])
		writer.writerows(subjects)

	# subject_counts = sorted([[subject, count] for subject, count in subject_count_dict.items()], key=lambda x: x[0])
	# subject_counts = sorted(subject_counts, key=lambda x: -x[1])
	#
	# with open('unique_subject_counts.csv', 'wb') as csvfile:
	# 	writer = csv.writer(csvfile)
	# 	writer.writerows(subject_counts)


if __name__ == "__main__":
	write_unique_subjects_by_tag_to_file()
