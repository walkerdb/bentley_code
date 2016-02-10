
def remove_vertical_tab_characters(filename):
    with open(filename, mode="rb") as f:
        data = f.read()

    data = data.decode("latin-1")
    data = data.encode("utf-8")

    name, extension = filename.split(".")
    with open("{}_clean.{}".format(name, extension), mode="wb") as f:
        f.write(data)


if __name__ == "__main__":
    remove_vertical_tab_characters("donor_records.tab")