import os
import re

from tqdm import tqdm


def fix_whitespace(input_dir, output_dir):
    whitespace_regex = r"\s{2,}|\v"
    eads = ["detroitnews.xml", "gonzalesjess.xml", "kevorkian.xml", "ovshinskyharv.xml", "pohrtkarl.xml"]
    # eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
    for ead in tqdm(eads):
        with open(os.path.join(input_dir, ead), mode="r") as f:
            data = f.read()

        data = " ".join(re.split(whitespace_regex, data))

        with open(os.path.join(output_dir, ead), mode="w") as f:
            f.write(data)


if __name__ == "__main__":
    input_directory = r"C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all"
    output_directory = r"C:\Users\wboyle\PycharmProjects\bentley_code\one-off scripts\output"
    fix_whitespace(input_dir=input_directory, output_dir=input_directory)
