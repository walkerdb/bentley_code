
def parse_famname(string, auth_id="", auth_source=""):
    auth_source = auth_source if auth_source else u"local"

    return {u"family_name": unicode(string), u"prefix": u"", u"sort_name_auto_generate": True, u"authority_id": auth_id, u"source": auth_source}