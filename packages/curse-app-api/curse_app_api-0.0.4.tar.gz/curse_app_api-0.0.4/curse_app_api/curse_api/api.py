from curse_app_api.utils import get_query, InvalidArgumentError, check_response, headers
from requests import session




class CurseAPI:
    def __init__(self):
        self._base_link = "https://addons-ecs.forgesvc.net/api/v2"
        self.__last_query_link = ""
        self.__last_response = None
        self.__web = None
        self.__init_web()

    def __init_web(self):
        self.__web = session()
        self.__web.headers = headers

    def search_addon(self, params=None, **kwargs):
        """

        :param params:
        :param kwargs:

        Search addon with the given parameters in params and kwargs dicts. If there are same keys in params and kwargs,
        the query will be served with params value.

        :return: if successful, returns list of dicts with info about mods found.
        """
        attr = {"categoryid": int, "gameid": int, "gameversion": str, "index": int, "pagesize": int,
                "searchfilter": str, "sectionid": int, "sort": int}
        if params is None:
            params = {}
        if type(params) != dict:
            raise InvalidArgumentError("'params' should be a dict object")
        search_params = f"/addon/search?"
        query = get_query(attr, params, kwargs)
        search_params += "&".join(f"{key}={value}" for key, value in query.items())
        self.__last_query_link = self._base_link + search_params
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def search_by_fingerprint(self, fingerprint: int):
        """
        Searches addon by file fingerprint
        :param fingerprint:
        :return:
        """
        self.__last_query_link = self._base_link + "/fingerprint"
        self.__last_response = self.__web.request("POST", self.__last_query_link, json=[fingerprint])
        return check_response(self.__last_response)

    def get_addon_description(self, addonID: int):
        params = f"/addon/{addonID}/description"
        self.__last_query_link = self._base_link + params
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response, "text")

    def get_addon_file_changelog(self, addonID: int, fileID: int):
        params = f"/addon/{addonID}/file/{fileID}/changelog"
        self.__last_query_link = self._base_link + params
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response, "text")

    def get_addon_file_download_url(self, addonID: int, fileID: int):
        params = f"/addon/{addonID}/file/{fileID}/download-url"
        self.__last_query_link = self._base_link + params
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response, "text")

    def get_addon_file_information(self, addonID: int, fileID: int):
        params = f"/addon/{addonID}/file/{fileID}"
        self.__last_query_link = self._base_link + params
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_addon_info(self, addonID: int):
        param = f"/addon/{addonID}"
        self.__last_query_link = self._base_link + param
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_addons_database_timestamp(self):
        self.__last_query_link = self._base_link + "/addon/timestamp"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_category_info(self, Categoryid: int):
        param = f"/category/{Categoryid}"
        self.__last_query_link = self._base_link + param
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_category_list(self):
        self.__last_query_link = self._base_link + "/category"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_category_section_info(self, SectionID: int):
        param = f"/category/section/{SectionID}"
        self.__last_query_link = self._base_link + param
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_category_timestamp(self):
        """
        Gets category timestamp
        :return: timestamp in 'str' format
        """
        self.__last_query_link = self._base_link + "/category/timestamp"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_featured_addons(self, params=None, **kwargs):
        attr = {"gameid": int, "addonids": list, "featuredcount": int, "popularcount": int, "updatedcount": int}
        if params is None:
            params = {}
        if type(params) != dict:
            raise InvalidArgumentError("params should be in a dictionary with keys:\n" +
                                       "\n".join("\'" + key + "\' with value of type: \'" + str(value) + "\'"
                                                 for key, value in attr.items()))
        query = get_query(attr, params, kwargs)
        self.__last_query_link = self._base_link + "/addon/featured"
        return self.__web.request("POST", self.__last_query_link, json=query).json(strict=False)

    def get_game_info(self, GameID: int):
        """
        Gets game info by its id
        :param GameID: id of game on curseforge
        :return:
        """
        self.__last_query_link = self._base_link + f"/game/{GameID}"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_game_timestamp(self):
        """
        Get game timestamp
        :return: timestamp in 'str' format
        """
        self.__last_query_link = self._base_link + "/game/timestamp"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_games_list(self, supportsAddons=None):
        """
        Returns games list, filtered by supportsAddons criteria. If it's None, it will return total games list
        :param supportsAddons: True or False
        :return: dict with info about games, filtered by supportsAddons criteria
        """
        self.__last_query_link = self._base_link + "/game"
        if supportsAddons is not None:
            if type(supportsAddons) == bool:
                self.__last_query_link += f"?supportsAddons={supportsAddons}"
            else:
                raise InvalidArgumentError("\'supportsAddons\' parameter should be True or False")
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_minecraft_version_info(self, VersionString: str):
        """
        Returns minecraft version info by given it's version in 'str' object

        Note: works on RELEASES only.
        :param VersionString: ex. "1.12.2"
        :return: dict with info about {VersionString} version of minecraft
        """
        param = f"/minecraft/version/{VersionString}"
        self.__last_query_link = self._base_link + param
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_minecraft_version_list(self):
        self.__last_query_link = self._base_link + "/minecraft/version"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_minecraft_version_timestamp(self):
        self.__last_query_link = self._base_link + "/minecraft/version/timestamp"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_modloader_info(self, VersionName: str):
        param = f"/minecraft/modloader/{VersionName}"
        self.__last_query_link = self._base_link + param
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return check_response(self.__last_response)

    def get_modloader_list(self):
        self.__last_query_link = self._base_link + "/minecraft/modloader"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_modloader_timestamp(self):
        self.__last_query_link = self._base_link + "/minecraft/modloader/timestamp"
        self.__last_response = self.__web.request("GET", self.__last_query_link)
        return self.__last_response.json(strict=False)

    def get_multiple_addons(self, params, *args):
        query = params + list(args)
        for e in query:
            if type(e) != int:
                raise InvalidArgumentError("parameters should be integer values.")
        self.__last_query_link = self._base_link + "/addon"
        self.__last_response = self.__web.request("POST", self.__last_query_link, json=query)
        return check_response(self.__last_response)
    
    @property
    def last_query_link(self):
        return self.__last_query_link
    
    @property
    def last_response(self):
        return self.__last_response
