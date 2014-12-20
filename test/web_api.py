__author__ = 'ict'

from steam_api import SteamAPI
import json
import pprint

api = SteamAPI()
data = api.invoke_web_api("ISteamApps", "GetAppList", 1)
data_json = json.loads(data.decode("utf8"))
pprint.pprint(data_json)