__author__ = 'ict'

import pickle
from ictsteam import *

profile_dir = "d:/steam_profile"
steam_id64 = "76561198118637711"
group_id = ""
profile_sum = 50000
save_step = 20
save_file = "crawler.save"
get_all_games = True
get_friends = True
player_priority_level = 8
group_priority_level = 8

if __name__ == "__main__":
    player_done_set = set()
    group_done_set = set()
    player_level_set = {l: set() for l in range(player_priority_level)}
    group_level_set = {l: set() for l in range(group_priority_level)}
    profile_sum_now = 0
    save_step_now = 0
    steam_id64_dict = {}
    group_id_dict = {}
    if profile_dir[-1] != os.sep:
        profile_dir += os.sep
    if steam_id64 != "":
        steam_id64_dict[steam_id64] = 0
        player_level_set[0].add(steam_id64)
    if group_id != "":
        group_id_dict[group_id] = 0
        group_level_set[0].add(group_id)
    if not os.path.exists(profile_dir):
        os.mkdir(profile_dir)
    else:
        file_list = os.listdir(profile_dir)
        for filename in file_list:
            player_done_set.add(filename[:-5])
        if os.path.exists(profile_dir + save_file):
            with open(profile_dir + save_file, "rb") as fp:
                pkg = pickle.load(fp)
                player_done_set = pkg[0]
                group_done_set = pkg[1]
                player_level_set = pkg[2]
                group_level_set = pkg[3]
                profile_sum_now = pkg[4]
                save_step_now = pkg[5]
                steam_id64_dict = pkg[6]
                group_id_dict = pkg[7]
    while (len(steam_id64_dict) != 0 or len(group_id_dict) != 0) and profile_sum_now < profile_sum:
        save_step_now += 1
        if save_step_now == save_step:
            save_step_now = 0
            with open(profile_dir + save_file, "wb") as fp:
                pkg = (
                    player_done_set,
                    group_done_set,
                    player_level_set,
                    group_level_set,
                    profile_sum_now,
                    save_step_now,
                    steam_id64_dict,
                    group_id_dict
                )
                pickle.dump(pkg, fp)
        while len(steam_id64_dict) == 0:
            if len(group_id_dict) == 0:
                break
            for l in range(group_priority_level - 1, -1, -1):
                if len(group_level_set[l]) > 0:
                    gid = group_level_set[l].pop()
                    del group_id_dict[gid]
                    break
            member_list = group_members_list(gid)
            if member_list is None:
                continue
            for member in member_list:
                if member not in player_done_set:
                    if member not in steam_id64_dict:
                        steam_id64_dict[member] = 0
                        player_level_set[0].add(member)
                    elif steam_id64_dict[member] < player_priority_level - 1:
                        player_level_set[steam_id64_dict[member]].remove(member)
                        steam_id64_dict[member] += 1
                        player_level_set[steam_id64_dict[member]].add(member)
            group_done_set.add(gid)
        if len(steam_id64_dict) == 0:
            continue
        level = 0
        for l in range(player_priority_level - 1, -1, -1):
            if len(player_level_set[l]) > 0:
                sid = player_level_set[l].pop()
                level = l
                del steam_id64_dict[sid]
                break
        pr = player_small_profile(sid, get_friends, get_all_games)
        if pr is None:
            continue
        if "friend" in pr:
            for one_friend in pr["friend"]:
                if one_friend not in player_done_set:
                    if one_friend not in steam_id64_dict:
                        steam_id64_dict[one_friend] = 0
                        player_level_set[0].add(one_friend)
                    elif steam_id64_dict[one_friend] < player_priority_level - 1:
                        player_level_set[steam_id64_dict[one_friend]].remove(one_friend)
                        steam_id64_dict[one_friend] += 1
                        player_level_set[steam_id64_dict[one_friend]].add(one_friend)
        group_list = pr["group"]
        if len(group_id_dict) <= 1024:
            for group in group_list:
                if group not in group_done_set:
                    if group not in group_id_dict:
                        group_id_dict[group] = 0
                        group_level_set[0].add(group)
                    elif group_id_dict[group] < group_priority_level - 1:
                        group_level_set[group_id_dict[group]].remove(group)
                        group_id_dict[group] += 1
                        group_level_set[group_id_dict[group]].add(group)
        json_dump(pr, profile_dir + pr["steamID64"] + ".json")
        profile_sum_now += 1
        player_done_set.add(sid)
        print("%d level:%d steamID64:%s steamID:%s" % (profile_sum_now, level, pr["steamID64"], pr["steamID"]))
    print("Done")
    print("Profile: %d, SteamID: %d, GroupID: %d" % (profile_sum_now, len(steam_id64_dict), len(group_id_dict)))