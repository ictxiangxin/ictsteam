__author__ = 'ict'

import httplib2
from xml.etree import ElementTree


def player_profile(steam_id64):
    if isinstance(steam_id64, int):
        url = "http://steamcommunity.com/profiles/%d/?xml=1" % steam_id64
    elif isinstance(steam_id64, str):
        url = "http://steamcommunity.com/profiles/%s/?xml=1" % steam_id64
    else:
        url = ""
    profile_et = http_xml_et(url)
    if profile_et is None:
        return None
    profile = {}
    for entry in profile_et.getchildren():
        if len(entry) > 0:
            sub_dict = {}
            for sub_entry in entry.getchildren():
                if len(sub_entry) > 0:
                    sub_sub_dict = {}
                    for sub_sub_entry in sub_entry.getchildren():
                        sub_sub_dict[sub_sub_entry.tag] = sub_sub_entry.text
                    if sub_entry.tag == "mostPlayedGame":
                        sub_sub_dict["gameID"] = sub_sub_dict["gameLink"][sub_sub_dict["gameLink"].rindex("/") + 1:]
                        if "hoursOnRecord" in sub_sub_dict:
                            sub_sub_dict["hoursOnRecord"] = float(sub_sub_dict["hoursOnRecord"].replace(",", ""))
                        if "hoursPlayed" in sub_sub_dict:
                            sub_sub_dict["hoursPlayed"] = float(sub_sub_dict["hoursPlayed"].replace(",", ""))
                        sub_dict[sub_sub_dict["gameName"]] = sub_sub_dict
                    elif sub_entry.tag == "group":
                        if "memberCount" in sub_sub_dict:
                            sub_sub_dict["memberCount"] = int(sub_sub_dict["memberCount"].replace(",", ""))
                        if "membersInChat" in sub_sub_dict:
                            sub_sub_dict["membersInChat"] = int(sub_sub_dict["membersInChat"].replace(",", ""))
                        if "membersInGame" in sub_sub_dict:
                            sub_sub_dict["membersInGame"] = int(sub_sub_dict["membersInGame"].replace(",", ""))
                        if "membersOnline" in sub_sub_dict:
                            sub_sub_dict["membersOnline"] = int(sub_sub_dict["membersOnline"].replace(",", ""))
                        sub_dict[sub_sub_dict["groupID64"]] = sub_sub_dict
                    else:
                        sub_dict[sub_entry.tag] = sub_sub_dict
                else:
                    sub_dict[sub_entry.tag] = sub_entry.text
            profile[entry.tag] = sub_dict
        else:
            profile[entry.tag] = entry.text
    return profile


def player_friends_list(steam_id64):
    if isinstance(steam_id64, int):
        url = "http://steamcommunity.com/profiles/%d/friends/?xml=1" % steam_id64
    elif isinstance(steam_id64, str):
        url = "http://steamcommunity.com/profiles/%s/friends/?xml=1" % steam_id64
    else:
        url = ""
    xml_et = http_xml_et(url)
    if xml_et is None:
        return None
    friends_et = None
    for entry in xml_et.getchildren():
        if entry.tag == "friends":
            friends_et = entry
    if friends_et is None:
        return []
    friends_list = []
    for entry in friends_et.getchildren():
        friends_list.append(entry.text)
    return friends_list


def player_games_list(steam_id64):
    if isinstance(steam_id64, int):
        url = "http://steamcommunity.com/profiles/%d/games/?xml=1" % steam_id64
    elif isinstance(steam_id64, str):
        url = "http://steamcommunity.com/profiles/%s/games/?xml=1" % steam_id64
    else:
        url = ""
    xml_et = http_xml_et(url)
    if xml_et is None:
        return None
    games_et = None
    for entry in xml_et.getchildren():
        if entry.tag == "games":
            games_et = entry
    games_list = []
    for entry in games_et.getchildren():
        tmp_dict = {}
        for sub_entry in entry.getchildren():
            if sub_entry.tag in ["appID", "hoursOnRecord", "hoursLast2Weeks"]:
                tmp_dict[sub_entry.tag] = sub_entry.text
        if "hoursOnRecord" not in tmp_dict:
            tmp_dict["hoursOnRecord"] = 0
        if "hoursLast2Weeks" not in tmp_dict:
            tmp_dict["hoursLast2Weeks"] = 0
        games_list.append((tmp_dict["appID"], tmp_dict["hoursOnRecord"], tmp_dict["hoursLast2Weeks"]))
    return games_list


def group_members_list(group_id):
    if isinstance(group_id, int):
        url = "http://steamcommunity.com/gid/%d/memberslistxml/?xml=1" % group_id
    elif isinstance(group_id, str):
        url = "http://steamcommunity.com/gid/%s/memberslistxml/?xml=1" % group_id
    else:
        url = ""
    xml_et = http_xml_et(url)
    if xml_et is None:
        return None
    members_et = None
    for entry in xml_et.getchildren():
        if entry.tag == "members":
            members_et = entry
    if members_et is None:
        return []
    members_list = []
    for entry in members_et.getchildren():
        members_list.append(entry.text)
    return members_list


def http_xml_et(url):
    http = httplib2.Http()
    response, content = http.request(url, "GET")
    if response["status"][0] != "2":
        return None
    try:
        xml_et = ElementTree.fromstring(content)
        return xml_et
    except RuntimeError:
        return None