# importing user agent
from .helpers import __user_agent


# importing webdrivers and options

from seleniumrequests import RequestMixin, Chrome as ChromeRequests
from selenium.webdriver import ChromeOptions
from msedge.selenium_tools.webdriver import WebDriver as Edge
from msedge.selenium_tools.options import Options as EdgeOptions

# importing managers
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager

import os


class WebDriverNotFoundError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


def prepare_chromium_options(options):
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("disable-gpu")
    options.add_argument(__user_agent)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return options


def prepare_edge_options(options):
    options.use_chromium = True
    return prepare_chromium_options(options)


class EdgeRequests(Edge, RequestMixin):
    pass


def get_driver():
    """

    :return: web_driver object for doing requests
    """
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
    os.environ['WDM_LOG_LEVEL'] = '0'
    drivers = {
        "chrome": {"driver": ChromeRequests, "manager": ChromeDriverManager,
                   "options": prepare_chromium_options(ChromeOptions())},
        "edge": {"driver": EdgeRequests, "manager": EdgeChromiumDriverManager,
                 "options": prepare_edge_options(EdgeOptions())}
    }
    driver = None
    for name, info in drivers.items():
        try:
            driver = info["driver"](executable_path=info["manager"]().install(), options=info["options"])
        except Exception:
            pass
    if driver is not None:
        return driver
    raise WebDriverNotFoundError("Unable to find webdriver for your OS")
