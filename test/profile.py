__author__ = 'ict'

from ictsteam import player_small_profile
from ictsteam import json_dump
from pprint import pprint

pr = player_small_profile(76561198118637711)
json_dump(pr, "d:/test.json")
pprint(pr)