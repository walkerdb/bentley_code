from utilities.ead_utilities.ead_utilities import EADDir

from uuid import uuid1

def add_uuids(ead):

    for i in range(10):
        tag = "c0" + str(i)
        for c0x in ead.tree.xpath("//" + tag):
            c0x.set("id", str(uuid1()))


def main():
    ead_dir = EADDir()
    ead_dir.apply_function_to_dir(add_uuids, output_dir=ead_dir.input_dir)


if __name__ == "__main__":
    main()