__author__ = 'ict'

import httplib2
from xml.etree import ElementTree


def player_profile(steam_id):
    if isinstance(steam_id, int):
        url = "http://steamcommunity.com/profiles/%d/?xml=1" % steam_id
    elif isinstance(steam_id, str):
        url = "http://steamcommunity.com/profiles/%s/?xml=1" % steam_id
    else:
        url = ""
    http = httplib2.Http()
    response, content = http.request(url, "GET")
    if response["status"][0] != "2":
        return None
    profile_et = ElementTree.fromstring(content)
    profile = {}
    for entry in profile_et.getchildren():
        if len(entry) > 0:
            sub_dict = {}
            for sub_entry in entry.getchildren():
                if len(sub_entry) > 0:
                    ssub_dict = {}
                    for ssub_entry in sub_entry.getchildren():
                        ssub_dict[ssub_entry.tag] = ssub_entry.text
                    if sub_entry.tag == "mostPlayedGame":
                        ssub_dict["gameID"] = ssub_dict["gameLink"][ssub_dict["gameLink"].rindex("/") + 1:]
                        if "hoursOnRecord" in ssub_dict:
                            ssub_dict["hoursOnRecord"] = float(ssub_dict["hoursOnRecord"])
                        if "hoursPlayed" in ssub_dict:
                            ssub_dict["hoursPlayed"] = float(ssub_dict["hoursPlayed"])
                        sub_dict[ssub_dict["gameName"]] = ssub_dict
                    elif sub_entry.tag == "group":
                        if "memberCount" in ssub_dict:
                            ssub_dict["memberCount"] = int(ssub_dict["memberCount"])
                        if "membersInChat" in ssub_dict:
                            ssub_dict["membersInChat"] = int(ssub_dict["membersInChat"])
                        if "membersInGame" in ssub_dict:
                            ssub_dict["membersInGame"] = int(ssub_dict["membersInGame"])
                        if "membersOnline" in ssub_dict:
                            ssub_dict["membersOnline"] = int(ssub_dict["membersOnline"])
                        sub_dict[ssub_dict["groupID64"]] = ssub_dict
                    else:
                        sub_dict[sub_entry.tag] = ssub_dict
                else:
                    sub_dict[sub_entry.tag] = sub_entry.text
            profile[entry.tag] = sub_dict
        else:
            profile[entry.tag] = entry.text
    return profile