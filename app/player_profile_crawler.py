__author__ = 'ict'

import pickle
from ictsteam import *

profile_dir = "d:/steam_profile"
steam_id64 = "76561198118637711"
group_id = ""
profile_sum = 50000
save_step = 100
save_file = "crawler.save"
get_all_games = True
get_friends = True

if __name__ == "__main__":
    already_set = set()
    if profile_dir[-1] != os.sep:
        profile_dir += os.sep
    steam_id64_set = set()
    group_id_set = set()
    if steam_id64 != "":
        steam_id64_set.add(steam_id64)
    if group_id != "":
        group_id_set.add(group_id)
    if not os.path.exists(profile_dir):
        os.mkdir(profile_dir)
    else:
        file_list = os.listdir(profile_dir)
        for filename in file_list:
            already_set.add(filename[:-5])
        if os.path.exists(profile_dir + save_file):
            with open(profile_dir + save_file, "rb") as fp:
                steam_id64_set, group_id_set = pickle.load(fp)
    profile_sum_now = 0
    save_step_now = 0
    while (len(steam_id64_set) != 0 or len(group_id_set) != 0) and profile_sum_now != profile_sum:
        save_step_now += 1
        if save_step_now == save_step:
            save_step_now = 0
            with open(profile_dir + save_file, "wb") as fp:
                pickle.dump((steam_id64_set, group_id_set), fp)
        while len(steam_id64_set) == 0:
            if len(group_id_set) == 0:
                break
            gid = group_id_set.pop()
            member_list = group_members_list(gid)
            if member_list is None:
                continue
            for member in member_list:
                steam_id64_set.add(member)
        if len(steam_id64_set) == 0:
            continue
        sid = steam_id64_set.pop()
        if sid in already_set:
            continue
        pr = player_small_profile(sid, get_friends, get_all_games)
        if pr is None:
            continue
        group_list = pr["group"]
        if len(group_id_set) <= 1024 * 1024:
            for group in group_list:
                group_id_set.add(group)
        json_dump(pr, profile_dir + pr["steamID64"] + ".json")
        profile_sum_now += 1
        print("%d/%d steamID64:%s steamID:%s" % (profile_sum_now, profile_sum, pr["steamID64"], pr["steamID"]))
    print("Done")
    print("Profile: %d, SteamID: %d, GroupID: %d" % (profile_sum_now, len(steam_id64_set), len(group_id_set)))