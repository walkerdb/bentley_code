import csv

from lxml import etree


def main():
    input_directory = 'S:\\Curation\\Projects\\Mellon\\ArchivesSpace\\ATeam_Migration\\EADs\\Real_Masters_all\\'
    output_directory = input_directory

    f = open("problem_files.csv", "w")
    f.close()
    filenames = set()
    total_changes = 0
    tags_left_alone = 0

    with open("emptytitles-updates.csv", mode="r") as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row)


        # To keep xpaths accurate as the program deletes and moves multiple nodes in a given xml file, it needs to make
        # changes from the end of the file to the front.
        for row in list(reversed(data)):
            filename = row[0]
            xpath = row[1]

            # if the program has already made a change to a given file and is queued to make another, it should edit the
            # altered version, and not the original.
            if filename in filenames:
                filedirectory = output_directory + filename
            else:
                filedirectory = input_directory + filename

            print("\nWorking on {0}, at {1}".format(filename, xpath))
            output = process_file(filedirectory, xpath)

            if output:  # process_file() returns an empty string if no changes are made
                total_changes += 1
                with open(output_directory + filename, mode="w") as f:
                    f.write(etree.tostring(output, pretty_print=True))
                filenames.add(filename)
            else:
                tags_left_alone += 1

        print("\nTotal changed tags: {0}".format(total_changes))
        print("Tags left alone: {0}".format(tags_left_alone))

    # moving things around and deleting nodes can result in some ugly formatting - needs to be prettified
    # prettifydirectory.prettify_xml_in_directory(output_directory, output_directory)

def process_file(filedirectory, xpath):
    """
    Coordinates edits to the root xml document based on a tag characterization of the problem node

    :param filedirectory: directory to the full XML file the problem node originates from
    :param xpath: xpath to the parent c0x node of the empty unittitle tag
    :return: if edits were made:
                returns an lxml etree representation of the full EAD containing new edits
             else:
                returns an empty string
    """

    full_ead_xml = etree.parse(filedirectory)
    parent_c0x = full_ead_xml.xpath(xpath)[0]

    # build dictionary of tags with text for use in characterizing the node
    tags_with_text_counts = build_tags_with_text_dict(parent_c0x)

    # if no tags have text, then the whole node can be deleted
    if len(tags_with_text_counts) == 0:
        remove_empty_node(parent_c0x)

    # the remaining characterizations depend on the presence of a container tag
    elif "container" in tags_with_text_counts:

        # If the container text of the problem node does not match that of its upper neighbor, change nothing
        if does_text_in_given_tag_change_in_upper_neighbor(parent_c0x, full_ead_xml, "container"):
            print("Container numbers change - no change made")
            record_problem_file(parent_c0x, full_ead_xml)
            return ""

        # if unitids change between problem node and upper neighbor, change nothing
        elif "unitid" in tags_with_text_counts:
            if does_text_in_given_tag_change_in_upper_neighbor(parent_c0x, full_ead_xml, "unitid"):
                print("Unitid numbers change - no change made")
                record_problem_file(parent_c0x, full_ead_xml)
                return ""

        # if the only content of the entire node is container numbers, remove node
        elif len(tags_with_text_counts) == 1:
            remove_node_with_did_content_only(parent_c0x, full_ead_xml)

        # if there is text in one other tag aside from the container tag, characterize further
        elif len(tags_with_text_counts) == 2:

            # actions for tags with content only in <container> and <odd> tags
            if "p" in tags_with_text_counts:
                odd_node = parent_c0x.xpath("odd")
                if len(odd_node) == 1:
                    odd_node = odd_node[0]
                    note_xpath = full_ead_xml.getpath(odd_node)
                    insert_node_into_upper_c0x_neighbor(full_ead_xml, note_xpath)
                    parent_c0x.getparent().remove(parent_c0x)
                else:
                    print("There is more than one note! Functionality not written.")
                    record_problem_file(parent_c0x, full_ead_xml)

            # extent actions
            elif "extent" in tags_with_text_counts:
                extent_node = parent_c0x.xpath("did/physdesc/extent")
                if len(extent_node) == 1:
                    extent_node = extent_node[0]
                    extent_xpath = full_ead_xml.getpath(extent_node)
                    insert_node_into_upper_c0x_neighbor(full_ead_xml, extent_xpath)
                    parent_c0x.getparent().remove(parent_c0x)
                else:
                    print("There is more than one extent! Functionality not written")
                    record_problem_file(parent_c0x, full_ead_xml)

            # other combinations are rare enough to to only handle manually
            else:
                print("Functionality not written for this tag combination. No actions taken")
                full_ead_xml = ""

        # past this point characterization becomes difficult
        else:
            print("Too many tags with text to process.")
            record_problem_file(parent_c0x, full_ead_xml)

    # catchall for anything else the program did not process
    else:
        print("No action taken")
        record_problem_file(parent_c0x, full_ead_xml)
        full_ead_xml = ""

    return full_ead_xml


def insert_node_into_upper_c0x_neighbor(full_ead_xml, xpath_of_node_to_move):
    node = full_ead_xml.xpath(xpath_of_node_to_move)[0]
    upper_neighbor_xpath = retrieve_upper_c0x_neighbor_xpath(full_ead_xml, xpath_of_node_to_move)
    upper_neighbor = full_ead_xml.xpath(upper_neighbor_xpath)[0]

    upper_neighbor_containers = upper_neighbor.xpath("did/container")
    if len(upper_neighbor_containers) == 0:
        # append container from node into upper neighbor
        print("Inserting containers from problem node into upper neighbor <did> tag.")

        c0x_parent = node
        is_c0x_level = False
        while not is_c0x_level:
            if c0x_parent.tag.startswith("c0"):
                is_c0x_level = True
            else:
                c0x_parent = c0x_parent.getparent()

        containers = c0x_parent.xpath("did/container")
        for container in containers:
            upper_neighbor[0].insert(1, container)

    if "extent" in node.tag:
        upper_neighbor[0].insert(1, node.getparent())
    else:
        upper_neighbor.insert(1, node)
    print("Inserted <{0}> node to upper neighbor, below <did> tag".format(node.tag))

def remove_empty_node(problem_c0x_node):
    problem_c0x_node.getparent().remove(problem_c0x_node)
    print("Removed empty node")


def remove_node_with_did_content_only(parent_c0x_node_of_unittitle, full_ead_xml):

    try:
        unittitle = parent_c0x_node_of_unittitle.xpath("did/unittitle")[0]
        unittitle_text = unittitle.text
    except:
        unittitle_text = ""

    if not unittitle_text:
        print("Removed node only containing a location or id (unchanged from upper neighbor)")
        parent_c0x_node_of_unittitle.getparent().remove(parent_c0x_node_of_unittitle)
    else:
        print("This should never happen, but I'm finding text in the unittitle")
        record_problem_file(parent_c0x_node_of_unittitle, full_ead_xml)


def does_text_in_given_tag_change_in_upper_neighbor(parent_c0x_node_of_unittitle, full_ead_xml, tag):
    """

    :param parent_c0x_node_of_unittitle: lxml etree representation of the c0x node parent of the problem unittitle tag
    :param full_ead_xml: lxml etree representation of full ead xml file
    :param tag: A child of a <did> tag - planned use case is for either container or unitid tags
    :return: True if tag text changes between origin and upper neighbor, else false
    """
    print("Checking if {0} numbers change".format(tag))
    containers = parent_c0x_node_of_unittitle.xpath("did/{0}".format(tag))
    num_original = []
    xpaths = set()
    num_upper_neighbor = []

    for container in containers:
        container_text = container.text
        if container_text:
            num_original.append(container_text)
            xpaths.add(full_ead_xml.getpath(container.getparent()))

    if len(xpaths) == 0:
        print("No {0}s found".format(tag))
        return True

    elif len(xpaths) == 1:
        upper_neighbor_xpath = retrieve_upper_c0x_neighbor_xpath(full_ead_xml, xpaths.pop())
        upper_neighbor = full_ead_xml.xpath(upper_neighbor_xpath)[0]
        upper_neighbor_containers = upper_neighbor.xpath("did/{0}".format(tag))
        for container in upper_neighbor_containers:
            if container.text:
                num_upper_neighbor.append(container.text)
    else:
        print("{0}s found in multiple tag locations. Wonky, so we'll leave this one for manual inspection".format(tag))
        return True

    if len(upper_neighbor_containers) == 0:
        print("no {0}s in upper neighbor. Returning 'false' for program to continue properly".format(tag))
        return False
    else:
        return num_original != num_upper_neighbor


def build_tags_with_text_dict(parent_c0x_node_of_unittitle):
    tags_with_text_counts = {}
    for tag in parent_c0x_node_of_unittitle.iter():
        text = tag.text
        if text:
            text = text.strip(" \n\t")
            if len(text) > 0:
                tags_with_text_counts[tag] = tags_with_text_counts.get(tag, 0) + 1

    return tags_with_text_counts


def retrieve_upper_c0x_neighbor_xpath(root_xml, xpath_to_target_node):
    """
    Upper c0x neighbor means whatever tag starting with "c0" first appears above the source c0x tag. This can be
    either a parent or a sibling.

    :param root_xml: source root xml for the entire document
    :param xpath_to_target_node: xpath to the node to find the upper c0x neighbor of
    :return: returns an xpath to the upper c0x neighbor
    """

    root_xml = etree.ElementTree(etree.fromstring(etree.tostring(root_xml)))
    node = root_xml.xpath(xpath_to_target_node)[0]

    is_c0x_level = False
    while not is_c0x_level:
        if node.tag.startswith("c0"):
            is_c0x_level = True
        else:
            node = node.getparent()

    upper_sibling = node.xpath("preceding-sibling::*")
    if len(upper_sibling) == 0:
        parent = node
        return root_xml.getpath(parent)
    else:
        if "did" in upper_sibling[-1].tag:
            return root_xml.getpath(node.getparent())
        else:
            return root_xml.getpath(upper_sibling[-1])


def record_problem_file(problem_node, xml):
    filename = problem_node.base.split("/")[-1]
    xpath = xml.getpath(problem_node)
    string = etree.tostring(problem_node)
    with open("problem_files.csv", mode='ab') as f:
        writer = csv.writer(f)
        writer.writerow([filename, xpath, string])
    print("Problem location recorded to file")

if __name__ == "__main__":
    main()