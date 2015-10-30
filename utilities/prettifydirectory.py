import re
import os
from os.path import join

from lxml import etree
from tqdm import tqdm


def prettify_xml_in_directory(input_dir, output_dir):
    eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
    eads = ["kevorkian.xml"]
    for filename in tqdm(eads, desc="Prettify progress", leave=True):

        text = prettify_xml(filename, input_dir, output_dir)

        # writing to file
        with open(join(output_dir, filename), mode="w") as f:
            f.write(text)


def prettify_xml(filename, input_dir, output_dir):
    parser = etree.XMLParser(remove_blank_text=True)

    # remove lists (lxml mungles them)
    text_without_lists, removed_lists = remove_lists_from_ead(os.path.join(input_dir, filename))

    # make lxml etree
    try:
        tree = etree.fromstring(text_without_lists).getroottree()
    except:
        # the above will fail if lists are not formatted correctly
        # fallback to parsing the whole ead
        tree = etree.parse(os.path.join(input_dir, filename))

    # read the tree with the custom parser
    with open(join(output_dir, filename), mode="w") as f:
        f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    new_tree = etree.parse(os.path.join(output_dir, filename), parser=parser)
    del tree

    # prettyprint
    with open(join(output_dir, filename), mode='w') as f:
        f.write(etree.tostring(new_tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))

    # re-iterate with the whitespace fix
    tree = etree.parse(join(output_dir, filename))
    fixed_text = fix_prettyprint_whitespace(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8"))

    # finally re-add the removed tags
    text = add_removed_lists(removed_lists, fixed_text)
    text = fix_indentation(text)

    return text


def extract_list(i, text):
    extracted_list = []
    depth = 0

    in_list = True
    while in_list:
        try:
            line = text[i].strip()
        except IndexError:
            print(text[0:20])
            break
        if line.startswith("<list"):
            depth += 1

        if line.startswith("</list") or (line.startswith("<list") and line.endswith("</list>")):
            depth -= 1
            if depth == 0:
                in_list = False

        extracted_list.append(text[i].strip("\n"))
        i += 1

    extracted_list = "\n".join(extracted_list)
    return i, extracted_list


def add_removed_lists(removed_lists, text):
    for i, list_ in enumerate(removed_lists):
        text = text.replace("$$$$LIST{0:0>5}".format(i), list_)
    return text


def remove_lists_from_ead(filepath):
    with open(filepath) as f:
        text = f.readlines()

    text_without_lists = []
    removed_lists = []

    i = 0
    count = 0
    while i < len(text):
        line = text[i].strip("\n")

        if line.strip().startswith("<list"):
            i, extracted_list = extract_list(i, text)
            text_without_lists[-1] += "\n$$$$LIST{0:0>5}".format(count)
            removed_lists.append(extracted_list)
            count += 1
            continue

        text_without_lists.append(line)
        i += 1

    return "\n".join(text_without_lists), removed_lists


def fix_indentation(text):
    split_text = text.split("\n")
    space_regex = r"^( *)"
    things_to_replace = ["><p>", "> <p>", "><head>", "> <head>"]
    replacements = [">\n{0}<p>", ">\n{0}<p>", ">\n{0}<head>", ">\n{0}<head>"]
    for i, line in enumerate(split_text):
        if all(thing not in line for thing in things_to_replace):
            continue

        space_count = len(re.findall(space_regex, split_text[i - 1])[0]) + 2

        new_line = line
        for j, thing in enumerate(things_to_replace):
            new_line = new_line.replace(thing, replacements[j].format(" " * space_count))

        split_text[i] = new_line

    return "\n".join(split_text)


def fix_prettyprint_whitespace(raw_text):
    open_to_close_tag_regex = r'(\<\/.*?\>)(\<[^\/]*?\>)'
    item_regex = r'(\<\/item\>)\ (\<item\>)'

    text = re.sub(open_to_close_tag_regex, r'\g<1> \g<2>', raw_text)
    text = re.sub(item_regex, r'\g<1>\g<2>', text)

    return text



if __name__ == "__main__":
    input_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    output_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    prettify_xml_in_directory(input_directory, output_directory)


