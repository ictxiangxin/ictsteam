__author__ = 'ict'

from ictsteam import *

player_list = []
player_list_file = "D:/members.txt"
profile_dir = "D:/member_profile"

if __name__ == "__main__":
    if player_list_file != "":
        with open(player_list_file, "r") as fp:
            player_data = fp.read()
            if "\r\n" in player_data:
                player_file_list = player_data.split("\r\n")
            else:
                player_file_list = player_data.split("\n")
            player_list += player_file_list
    if profile_dir[-1] != os.sep:
        profile_dir += os.sep
    if not os.path.exists(profile_dir):
        os.mkdir(profile_dir)
    for player in player_list:
        pr = player_small_profile(player)
        if pr is None:
            continue
        json_dump(pr, profile_dir + pr["steamID64"] + ".json")
        print("steamID64:%s steamID:%s" % (pr["steamID64"], pr["steamID"]))