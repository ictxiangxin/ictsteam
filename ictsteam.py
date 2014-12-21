__author__ = 'ict'

from community import *
from steam_api import *


def json_dump(profile, filename):
    with open(filename, "w") as fp:
        json.dump(profile, fp, indent=True)


def player_small_profile(steam_id64):
    profile = player_profile(steam_id64)
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
    if "groups" in profile:
        small_profile["group"] = list(profile["groups"])
    else:
        small_profile["group"] = []
    small_profile["game"] = []
    if "mostPlayedGames" in profile:
        for _, game in profile["mostPlayedGames"].items():
            small_profile["game"].append((game["gameID"], game["hoursOnRecord"], game["hoursPlayed"]))
    return small_profile


def update_local_steam_api():
    tmp_steam_api = SteamAPI()
    tmp_steam_api.update_api_file()