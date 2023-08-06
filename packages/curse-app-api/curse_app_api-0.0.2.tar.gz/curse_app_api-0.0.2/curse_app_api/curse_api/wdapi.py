from .api import CurseAPI
from curse_app_api.utils import get_driver


class WDCurseAPI(CurseAPI):
    def __init_web(self):
        self.__web = get_driver()
