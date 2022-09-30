from http.cookiejar import Cookie, CookieJar
from http.cookies import CookieError
from pathlib import Path
from time import time
from typing import Any, Union

import browser_cookie3
from requests import HTTPError, Response


def _order(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        if order["order_id"] == obj_id:
            return order
    raise ValueError(f"order with id = {repr(obj_id)} doesn't exist.")


def _item(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        for item in order["order_items"]:
            if item["item_id"] == obj_id:
                return order
    raise ValueError(f"order item with id = {repr(obj_id)} doesn't exist.")


def _restaurant(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        if order["restaurant_id"] == obj_id:
            return order
    raise ValueError(f"restaurant with id = {repr(obj_id)} doesn't exist.")


def _address(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
    **kwargs: dict[str, Any],
) -> dict:
    ddav = kwargs["ddav"]
    ver = kwargs["ver"]
    for order in order_list:
        if all(
            (
                ddav is True,
                order["delivery_address"]["id"] == obj_id,
                order["delivery_address"]["version"] == ver,
            )
        ):
            return order
        if ddav is False and order["delivery_address"]["id"] == obj_id:
            return order
    raise ValueError(
        f"Address with (id,ver) = ({obj_id},{ver}) doesn't exist."
    ) if ddav else ValueError(f"Address with id = {obj_id} doesn't exist.")


def _payment(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        if order["transactionId"] == obj_id:
            return order
    raise ValueError(f"payment with transaction id = {repr(obj_id)} doesn't exist.")


def _offer(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        for offer in order["offers_data"]:
            if offer["id"] == obj_id:
                return order
    raise ValueError(f"Address with id = {repr(obj_id)} doesn't exist.")


def find_order(
    obj: str,
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
    **kwargs: dict[str, Any],
) -> dict:

    if obj == "address":
        return _address(order_list, obj_id, **kwargs)

    obj_dict = {
        "order": _order,
        "item": _item,
        "restaurant": _restaurant,
        "payment": _payment,
        "offer": _offer,
    }
    return obj_dict[obj](order_list, obj_id)


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


def create_save_path(path_: Path) -> None:
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
