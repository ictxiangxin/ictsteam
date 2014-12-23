__author__ = 'ict'

from community import *
from steam_api import *


def json_dump(profile, filename):
    with open(filename, "w") as fp:
        json.dump(profile, fp, indent=True)


def player_small_profile(steam_id64, get_friends=True, get_all_games=True):
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
    if get_friends:
            friends = player_friends_list(steam_id64)
            if friends is not None:
                small_profile["friend"] = friends
    if get_all_games:
        games = player_games_list(steam_id64)
        if games is not None:
            small_profile["game"] = games
    return small_profile


def update_local_steam_api():
    tmp_steam_api = SteamAPI()
    tmp_steam_api.update_api_file()


def steam_game_dict(api=None):
    if api is None:
        api = SteamAPI()
    game_list_json = json.loads(api.invoke_web_api("ISteamApps", "GetAppList", "2").decode("utf8"))
    game_list_json = game_list_json["applist"]["apps"]
    game_dict = {}
    for game_info in game_list_json:
        game_dict[game_info["appid"]] = game_info["name"]
    return game_dict