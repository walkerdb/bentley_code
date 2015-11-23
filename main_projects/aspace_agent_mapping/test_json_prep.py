import unittest


from parsers.test_parse_persname import TestParsePersname

unittest.main()


def make_date_json(type_, label, expression="", begin_date="", end_date=""):
    return {"date_type": type_, "label": label, 'expression': expression, "begin": begin_date, "end": end_date}
