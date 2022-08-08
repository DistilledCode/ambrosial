from ast import literal_eval
from dataclasses import make_dataclass
from typing import Optional

import browser_cookie3
from requests import Response, get


def _literal_eval(val: str):
    try:
        return literal_eval(val)
    except SyntaxError:
        return val
    except ValueError:
        return val


def recursive_evaluation(obj: dict):
    try:
        items = obj.items()
    except AttributeError:
        return obj
    for key, val in items:
        if val.__class__ is list:
            for ind, i in enumerate(val):
                val[ind] = recursive_evaluation(i)
        if val.__class__ is str:
            obj[key] = _literal_eval(val)
        if val.__class__ is dict:
            obj[key] = recursive_evaluation(val)
    return obj


def dict2dataclass(name: str, dict_to_conv: dict, **kwargs: dict) -> type:
    if any(not isinstance(key, str) for key in dict_to_conv):
        raise TypeError(f"Field names must be valid identifiers: {key!r}")
    if any(not key.replace(" ", "_").isidentifier() for key in dict_to_conv):
        raise TypeError(f"Field names must be valid identifiers: {key!r}")
    field_list = []
    for key, val in dict_to_conv.items():
        new_key = key.replace(" ", "_").lower()
        if val.__class__ in [list, set, tuple]:
            value_list = []
            for ind, i in enumerate(val):
                if i.__class__ is dict:
                    value_list.append(dict2dataclass(f"{new_key}{ind}", i, **kwargs))
                else:
                    value_list.append(i)
            val = tuple(value_list)
        if val.__class__ is dict:
            val = dict2dataclass(new_key, val, **kwargs)
        field_list.append((new_key, val.__class__, val))
    DataClass = make_dataclass(name, field_list, **kwargs)
    return DataClass()


def _req_dump(order_id: Optional[int]) -> Response:
    if order_id is None:
        param = {}
    else:
        param = {"order_id": order_id}
    URL = "https://www.swiggy.com/dapi/order/all"
    cookie_jar = browser_cookie3.load("www.swiggy.com")
    return get(URL, cookies=cookie_jar, params=param)


def _valid_response(response: Response):
    if not response.status_code == 200:
        # TODO: Log this
        return False, response.reason
    resp_json = response.json()
    if not resp_json["statusCode"] == 0:
        # TODO: Log this
        return False, resp_json["statusMessage"]
    return True, None


def _exhausted(response: Response):
    if not (v := _valid_response(response))[0]:
        print(v[1])
    return not bool(response.json()["data"]["orders"])


def _order_list(response: Response):
    if not (v := _valid_response(response))[0]:
        print(v[1])
    return [order for order in response.json()["data"]["orders"]]


def get_orders():
    first_response = _req_dump(order_id=None)
    orders = []
    orders.extend(_order_list(first_response))
    while _exhausted(r := _req_dump(order_id=orders[-1]["order_id"])) is False:
        orders.extend(_order_list(r))
        print(f"\r Retrieved {len(orders):>4} orders", end="")
    print()
    return orders
