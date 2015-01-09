__author__ = 'ict'

import json
import os


profile_dir = "d:/steam_profile"
graph_file = "d:/steam_friend.txt"
game_mark_file = "d:/steam_game.txt"
mapping_file = "d:/steam_mapping.csv"
number_base = 1
close_loop = True
max_sum = 500000

if __name__ == "__main__":
    steam_id64_mapping = {}
    steam_game_mapping = {}
    id64_game_mapping = {}
    game_player = {}
    graph = set()
    forbidden_node = set()
    count = number_base
    game_count = 1
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
                if count - number_base >= max_sum:
                    break
            if "friend" in pr:
                most_time = 0
                most_game = "0"
                if "mostgame" in pr and len(pr["mostgame"]) != 0:
                    for game_id, total_time, _ in pr["mostgame"]:
                        if total_time > most_time and game_id != "10" and game_id != "240":
                            most_time = total_time
                            most_game = game_id
                if "game" in pr and most_game == "0":
                    for game_id, total_time, _ in pr["game"]:
                        if not isinstance(total_time, float):
                            total_time = float(str(total_time).replace(",", ""))
                        if total_time > most_time and game_id != "10" and game_id != "240":
                            most_time = total_time
                            most_game = game_id
                if most_game == "10" or most_game == "240":
                    most_game = "730"
                if most_game not in steam_game_mapping:
                    steam_game_mapping[most_game] = game_count
                    game_count += 1
                id64_game_mapping[steam_id64_mapping[sid]] = steam_game_mapping[most_game]
                if steam_game_mapping[most_game] not in game_player:
                    game_player[steam_game_mapping[most_game]] = [steam_id64_mapping[sid]]
                if steam_game_mapping[most_game] not in game_player:
                    game_player[steam_game_mapping[most_game]] = []
                game_player[steam_game_mapping[most_game]].append(steam_id64_mapping[sid])
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
            else:
                forbidden_node.add(steam_id64_mapping[sid])
    new_graph = set()
    mark_mapping = {}
    mark_count = 1
    for mark, nodes in game_player.items():
        if len(nodes) / len(steam_id64_mapping) < 0.01:
            for node in nodes:
                forbidden_node.add(node)
        else:
            mark_mapping[mark] = mark_count
            mark_count += 1
    node_mapping = {}
    new_id64_game_mapping = {}
    count = number_base
    for edge in graph:
        if edge[0] not in forbidden_node and edge[1] not in forbidden_node:
            if edge[0] not in node_mapping:
                node_mapping[edge[0]] = count
                new_id64_game_mapping[count] = id64_game_mapping[edge[0]]
                count += 1
            if edge[1] not in node_mapping:
                node_mapping[edge[1]] = count
                new_id64_game_mapping[count] = id64_game_mapping[edge[1]]
                count += 1
            new_graph.add(edge)
    with open(graph_file, "w") as fp:
        fp.write("%d\n" % len(node_mapping))
        for edge in new_graph:
            fp.write("%d\t%d\n" % (node_mapping[edge[0]], node_mapping[edge[1]]))
            fp.write("%d\t%d\n" % (node_mapping[edge[1]], node_mapping[edge[0]]))
    with open(mapping_file, "w") as fp:
        for steam_id64, number in steam_id64_mapping.items():
            fp.write("%s, %d\n" % (steam_id64, number))
    with open(game_mark_file, "w") as fp:
        id64_game_list = list(new_id64_game_mapping.items())
        id64_game_list.sort()
        print(steam_game_mapping)
        fp.write(" ".join([str(mark_mapping[mark]) for _, mark in id64_game_list]))