import csv
import apache_log_parser
from tqdm import tqdm

parser = apache_log_parser.make_parser("%h %t \"%U\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %v")

with open("bhlead_201509_semi_anon.txt", mode="r") as f:
    logs = f.readlines()

parsed_lines = []
for log in tqdm(logs):
    parsed_line = parser(log)
    parsed_lines.append(parsed_line)

keys = sorted(parsed_lines[0].keys())

with open("output.csv", mode="wb") as f:
    writer = csv.writer(f)
    writer.writerow(keys)
    for line in parsed_lines:
        writer.writerow([line.get(key, "") for key in keys])
