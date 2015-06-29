import csv
import os

from lxml import etree

input_dir = '/Users/BHLStaff/PycharmProjects/vandura/Real_Masters_all'

files = [file for file in os.listdir(input_dir) if file.endswith(".xml")]

for file in files:
