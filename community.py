__author__ = 'ict'

import httplib2
from xml.etree import ElementTree
import json


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
    try:
        profile_et = ElementTree.fromstring(content)
    except:
        return None
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
                            ssub_dict["hoursOnRecord"] = float(ssub_dict["hoursOnRecord"].replace(",", ""))
                        if "hoursPlayed" in ssub_dict:
                            ssub_dict["hoursPlayed"] = float(ssub_dict["hoursPlayed"].replace(",", ""))
                        sub_dict[ssub_dict["gameName"]] = ssub_dict
                    elif sub_entry.tag == "group":
                        if "memberCount" in ssub_dict:
                            ssub_dict["memberCount"] = int(ssub_dict["memberCount"].replace(",", ""))
                        if "membersInChat" in ssub_dict:
                            ssub_dict["membersInChat"] = int(ssub_dict["membersInChat"].replace(",", ""))
                        if "membersInGame" in ssub_dict:
                            ssub_dict["membersInGame"] = int(ssub_dict["membersInGame"].replace(",", ""))
                        if "membersOnline" in ssub_dict:
                            ssub_dict["membersOnline"] = int(ssub_dict["membersOnline"].replace(",", ""))
                        sub_dict[ssub_dict["groupID64"]] = ssub_dict
                    else:
                        sub_dict[sub_entry.tag] = ssub_dict
                else:
                    sub_dict[sub_entry.tag] = sub_entry.text
            profile[entry.tag] = sub_dict
        else:
            profile[entry.tag] = entry.text
    return profile


def player_small_profile(steam_id):
    print(steam_id)
    profile = player_profile(steam_id)
    if profile is None:
        return None
    if "visibilityState" not in profile:
        return None
    if profile["visibilityState"] == "1":
        return None
    small_profile = dict()
    small_profile["steamID"] = profile["steamID"]
    small_profile["steamID64"] = profile["steamID64"]
    small_profile["memberSince"] = profile["memberSince"]
    small_profile["group"] = list(profile["groups"])
    small_profile["game"] = []
    if "mostPlayedGames" in profile:
        for _, game in profile["mostPlayedGames"].items():
            small_profile["game"].append((game["gameID"], game["hoursOnRecord"], game["hoursPlayed"]))
    return small_profile


def json_dump(profile, filename):
    with open(filename, "w") as fp:
        json.dump(profile, fp, indent=True)


def group_memberslist(group_id):
    if isinstance(group_id, int):
        url = "http://steamcommunity.com/gid/%d/memberslistxml/?xml=1" % group_id
    elif isinstance(group_id, str):
        url = "http://steamcommunity.com/gid/%s/memberslistxml/?xml=1" % group_id
    else:
        url = ""
    http = httplib2.Http()
    response, content = http.request(url, "GET")
    if response["status"][0] != "2":
        return None
    try:
        profile_et = ElementTree.fromstring(content)
    except:
        return None
    members_et = None
    for entry in profile_et.getchildren():
        if entry.tag == "members":
            members_et = entry
    if members_et is None:
        return []
    memberslist = []
    for entry in members_et:
        memberslist.append(entry.text)
    return memberslist