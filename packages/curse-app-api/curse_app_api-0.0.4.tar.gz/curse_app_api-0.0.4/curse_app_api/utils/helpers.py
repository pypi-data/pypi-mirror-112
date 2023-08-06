from requests import Response
import json

__user_agent = (
    "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
    + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
)
headers = {"User-Agent": __user_agent}


class InvalidArgumentError(Exception):
    def __init__(self, *args):
        super().__init__("Invalid argument(s): " + " ".join(str(e) for e in args))


def get_query(attr: dict, *args):
    """

    :param attr:
    :param args: list of dicts

    For each dict in args it checks that key in in attr and value type is attr[key].
    If there are same keys from different dicts, the first occurrence will be returned.

    :return: dict merged from args
    """
    query = {}
    for arg in args:
        for key, value in arg.items():
            k = key.lower()
            if k not in attr:
                raise InvalidArgumentError(f"'{key}'")
            elif type(value) != attr[key.lower()]:
                raise InvalidArgumentError(f"'{key}' should have type: {attr[k]}, while type"
                                           f" of value is {type(value)}")
            elif query.get(k, None) is None:
                query[k] = value
    return query


def check_response(resp: Response, return_type: str = "json"):
    """

    It checks that request was successful and returns data.
    If request was unsuccessful, returns empty object, depending on return_type

    :param resp: Response for checking
    :param return_type: 'json' or 'text', by default 'json' because most methods returns JSON objects
    :return:
    """
    if return_type == "text":
        if resp.status_code == 200:
            return resp.text
        return ""
    if return_type == "json":
        if resp.status_code == 200:
            return resp.json(strict=False)
        return {}


def pretty_json_string(json_string: str, indent: int = 4, ensure_ascii: bool = True):
    """

    Function for creating more easy-to-read json object from one-line string.
    If it fails, string is not json type, so it will be returned as result

    :param json_string:
    :param indent: by default sets to 4
    :param ensure_ascii: True or False, by default sets to True
    :return: resulted string
    """
    try:
        return json.dumps(json_string, indent=indent, ensure_ascii=ensure_ascii)
    except json.JSONDecodeError:
        return json_string
