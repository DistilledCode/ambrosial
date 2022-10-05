from http.cookiejar import Cookie, CookieJar
from http.cookies import CookieError
from pathlib import Path
from time import time
from typing import TypedDict

import browser_cookie3
from requests import HTTPError, Response


# total=False to satisfy MyPy
class UserInfo(TypedDict, total=False):

    customer_id: int
    name: str
    mobile: str
    email: str
    emailVerified: bool
    super_status: str
    user_registered: str


def get_empty_sid() -> Cookie:
    return Cookie(
        version=0,
        name="_sid",
        value="0",
        port=None,
        port_specified=False,
        domain="www.swiggy.com",
        domain_specified=True,
        domain_initial_dot=True,
        path="/",
        path_specified=True,
        secure=True,
        expires=int(time()) + 31536000,  # +1 year
        discard=True,
        comment=None,
        comment_url=None,
        rfc2109=False,
        rest={"HTTPOnly": ""},
    )


def create_path(path_: Path) -> None:
    if path_.exists() is False:
        path_.mkdir(parents=True, exist_ok=True)


def validate_response(response: Response) -> None:
    response.raise_for_status()
    resp_json = response.json()
    if not resp_json["statusCode"] == 0:
        raise HTTPError(f"Bad Response: {resp_json['statusMessage']}")


def get_cookies(domain_name: str) -> CookieJar:
    cookie_jar = browser_cookie3.load(domain_name)
    if not len(cookie_jar) > 0:
        raise CookieError(f"{repr(domain_name)}: No cookies found.")
    return cookie_jar
