__author__ = 'ict'

import json
import httplib2
import os


class SteamAPI:
    def __init__(self):
        self.__api_file = os.path.dirname(__file__) + os.sep + "steam_web_api.json"
        self.__api_site = "http://api.steampowered.com/"
        self.__api_json = None
        with open(self.__api_file, "r") as fp:
            self.__api = json.load(fp)
        self.__api_json = self.__api["apilist"]["interfaces"]
        self.__api = {}
        for one_api in self.__api_json:
            method = one_api["methods"]
            self.__api[one_api["name"]] = {}
            for one_method in method:
                self.__api[one_api["name"]][one_method["name"]] = one_method

    def update_api_file(self):
        new_api_file_content = self.invoke_web_api("ISteamWebAPIUtil", "GetSupportedAPIList", 1)
        with open(self.__api_file, "wb") as fp:
            fp.write(new_api_file_content)

    def invoke_web_api(self, interface, method, method_version, args=None):
        if interface in self.__api:
            if method in self.__api[interface]:
                http_method = self.__api[interface][method]["httpmethod"]
                uri = str(interface) + "/" + str(method) + "/" + ("v%4s" % method_version).replace(" ", "0") + "/"
                if args is not None:
                    uri += "?" + str(args)[1:-1].replace("\'", "").replace(": ", "=").replace(", ", "&")
                http = httplib2.Http()
                url = self.__api_site + uri
                response, content = http.request(url, http_method)
                if response["status"][0] == "2":
                    return content
        return None