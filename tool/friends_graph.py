__author__ = 'ict'

import json
import os


profile_dir = "d:/steam_profile"
graph_file = "d:/steam_friend.csv"
mapping_file = "d:/steam_mapping.csv"
number_base = 1
close_loop = True

if __name__ == "__main__":
    steam_id64_mapping = {}
    graph = set()
    count = number_base
    if profile_dir[-1] != os.sep:
        profile_dir += os.sep
    lock_id = None
    if close_loop:
        lock_id = set([filename[:-5] for filename in os.listdir(profile_dir)])
    for filename in os.listdir(profile_dir):
        if filename[-5:] == ".json":
            print("Parsing: %s" % filename)
            with open(profile_dir + filename, "r") as fp:
                pr = json.load(fp)
            sid = pr["steamID64"]
            if sid not in steam_id64_mapping:
                steam_id64_mapping[sid] = count
                count += 1
            if "friend" in pr:
                for friend in pr["friend"]:
                    if lock_id is not None:
                        if friend not in lock_id:
                            continue
                    if friend not in steam_id64_mapping:
                        steam_id64_mapping[friend] = count
                        count += 1
                    a = steam_id64_mapping[sid]
                    b = steam_id64_mapping[friend]
                    if a < b:
                        graph.add((a, b))
                    else:
                        graph.add((b, a))
    with open(graph_file, "w") as fp:
        for edge in graph:
            fp.write("%d, %d\n" % (edge[0], edge[1]))
    with open(mapping_file, "w") as fp:
        for steam_id64, number in steam_id64_mapping.items():
            fp.write("%s, %d\n" % (steam_id64, number))