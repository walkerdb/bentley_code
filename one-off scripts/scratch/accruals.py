import csv
from utilities.utilities import EADDir


def get_multiple_accruals(ead):
    accruals = ead.tree.xpath("//accruals")

    if len(accruals) > 1:
        return [ead.filename, "{} accruals".format(len(accruals))]

    return ""


if __name__ == "__main__":
    ead_dir = EADDir()
    results = list(filter(None, ead_dir.characterize_dir(get_multiple_accruals)))

    with open("multiple_accruals.csv", mode="wb") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "accrual number"])
        writer.writerows(results)
