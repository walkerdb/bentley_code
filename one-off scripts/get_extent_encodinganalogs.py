import csv
import os

from lxml import etree

input_dir = '/Users/BHLStaff/PycharmProjects/vandura/Real_Masters_all'

files = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]

for ead in files:
	pass
