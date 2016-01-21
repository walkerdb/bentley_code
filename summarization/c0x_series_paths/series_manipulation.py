from os import listdir
from os import path

from lxml import etree
from tqdm import tqdm


input_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'


def replace_wonky_level_paths(tree, filename, tag="c0", attribute="level"):
    dsc_tree_children = list(tree.xpath("/ead/archdesc/dsc")[0])
    path_breadcrumb_list = []
    wonky_series_path = "item->file"

    # recursion function
    def recurse_down_tree(node):
        path_level_text = node.get(attribute)

        # add current level to series breadcrumb path
        path_breadcrumb_list.append(path_level_text)
        path_breadcrumb_string = "->".join([str(level) for level in path_breadcrumb_list])

        if wonky_series_path in path_breadcrumb_string[-11:]:
            node.getparent().attrib["level"] = "file"
            path_breadcrumb_list.pop()
            path_breadcrumb_list.pop()
            path_breadcrumb_list.append("file")
            path_breadcrumb_list.append("file")

        # for each child in the current node that starts with the named tag, recurse
        for child in list(node):
            if child.tag.startswith(tag):
                recurse_down_tree(child)

        # if the code reaches this point, this is the end of this branch of the tree, so remove this leaf of the tree
        # from the path breadcrumb list
        path_breadcrumb_list.pop()

    # control loop
    for node in dsc_tree_children:
        if node.tag.startswith("c0"):
            recurse_down_tree(node)

    with open(path.join(input_directory, filename), mode="w") as f:
        f.write(etree.tostring(tree))


if __name__ == "__main__":
    for filename in tqdm(listdir(input_directory)):
        if filename.endswith(".xml"):
            tree = etree.parse(path.join(input_directory, filename))
            replace_wonky_level_paths(tree, filename)
