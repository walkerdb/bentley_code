import csv
from os import path, listdir
import re

from tqdm import tqdm

def fix_prettyprint_whitespace(raw_text):
	open_to_close_tag_regex = r'(\<\/.*?\>)(\<[^\/]*?\>)'
	item_regex = r'(\<\/item\>)\ (\<item\>)'
	double_spaced_tag_regex = r'(\ \<.*?\>)\ '

	text = re.sub(open_to_close_tag_regex, r'\g<1> \g<2>', raw_text)
	text = re.sub(item_regex, r'\g<1>\g<2>', text)
	text = re.sub(double_spaced_tag_regex, r'\g<1>', text)
	return text


if __name__ == "__main__":
	input_dir = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
	output_dir = r'C:\Users\wboyle\PycharmProjects\bentley_code\one-off scripts\prettyprint_whitespace_fix\output'
	for ead in tqdm([ead for ead in listdir(input_dir) if ead.endswith(".xml")]):
		with open(path.join(input_dir, ead), mode="r") as f:
			raw_text = f.read()
		reconstructed = fix_prettyprint_whitespace(raw_text)
		with open(path.join(output_dir, ead), mode="w") as f:
			f.write(reconstructed)
