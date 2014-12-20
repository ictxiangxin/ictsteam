__author__ = 'ict'

import httplib2
from xml.etree import ElementTree


def player_profile(steam_id):
    url = ""
    if isinstance(steam_id, int):
        url = "http://steamcommunity.com/profiles/%d/?xml=1" % steam_id
    elif isinstance(steam_id, str):
        url = "http://steamcommunity.com/profiles/%s/?xml=1" % steam_id
    http = httplib2.Http()
    response, content = http.request(url, "GET")
    if response["status"][0] != "2":
        return None
    profile_et = ElementTree.fromstring(content)
    tmp_read(profile_et)


def tmp_read(et):
    if isinstance(et, ElementTree.Element):
        for e in et:
            tmp_read(e)
            print(e)