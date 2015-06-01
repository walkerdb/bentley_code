import csv
import extent_splitter


CHARACTERIZE = False


def main():
	output = []
	longest_statement = 0
	filename = "all_extents.csv"
	print(filename)
	with open(filename, mode="r") as f:
		reader = csv.reader(f)
		for extent_row in reader:
			ead_filename = extent_row[0]
			extent_xpath = extent_row[1]
			extent_statement = extent_row[2]
			split_extents = extent_splitter.split_extents(extent_statement)
			row = [ead_filename, extent_xpath, extent_statement]

			if CHARACTERIZE:
				for extent in split_extents:
					row.append(extent)
				output.append(row)

				# keeping track of the longest line in the csv, so that we can add
				if len(split_extents) > longest_statement:
					longest_statement = len(split_extents)
			else:
				row.append(split_extents)
				output.append(row)

	with open("split_extents.csv", mode="wb") as f:
		writer = csv.writer(f)
		if CHARACTERIZE:
			for row in output:
				if len(row) < longest_statement:
					diff = longest_statement - len(row)
					row = add_blank_elements(row, diff)
				writer.writerow(row)
		else:
			writer.writerows(output)


def add_blank_elements(row, number_of_elements):
	i = 0
	while i < number_of_elements:
		row.append("")
		i += 1

	return row


if __name__ == "__main__":
	main()