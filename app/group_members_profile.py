__author__ = 'ict'

from ictsteam import *

group_list = [
    103582791432317220,
    103582791432300003,
    103582791432689852,
    103582791433277036,
    103582791432457214,
    103582791432836422,
]
group_list_file = ""
members_file = "D:/members.txt"

if __name__ == "__main__":
    player_set = set()
    if group_list_file != "":
        with open(group_list_file, "r") as fp:
            group_data = fp.read()
            if "\r\n" in group_data:
                group_file_list = group_data.split("\r\n")
            else:
                group_file_list = group_data.split("\n")
            group_list += group_file_list
    for group in group_list:
        members_list = group_members_list(group)
        for member in members_list:
            player_set.add(member)
    with open(members_file, "w") as fp:
        for player in player_set:
            fp.write(player + "\n")