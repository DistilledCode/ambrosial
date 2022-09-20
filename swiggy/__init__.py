from ast import literal_eval
from copy import deepcopy
from itertools import chain
from json import JSONDecodeError, dump, load
from pathlib import Path
from typing import Optional
from warnings import warn

import browser_cookie3
from msgpack import pack, unpack
from requests import HTTPError, get

import swiggy.convert as convert
from swiggy.convert import attrs


class Swiggy:
    def __init__(self, ddav: bool = False):
        self.ddav = ddav
        self._o_url = "https://www.swiggy.com/dapi/order/all"
        self._p_url = "https://www.swiggy.com/mapi/profile/info"
        self._cookie_jar = browser_cookie3.load("www.swiggy.com")
        self.orders_r = []
        self.orders_p = []
        self._response = None
        self._resp_json = dict()
        self._invalid_reason = ""
        self._customer_info = dict()
        self._fetched = False
        self._create_save_path()

    def _create_save_path(self):
        path = Path(__file__).resolve().parents[1] / "data"
        if path.exists() is False:
            path.mkdir(parents=True, exist_ok=True)

    def account_info(self):
        if self._customer_info:
            return self._customer_info
        self._response = get(self._p_url, cookies=self._cookie_jar)
        self._resp_json = self._response.json()
        self._validate_response()
        data = self._resp_json["data"]
        self._customer_info = {
            "customer_id": data["customer_id"],
            "name": data["name"],
            "mobile": data["mobile"],
            "email": data["email"],
            "emailVerified": data["emailVerified"],
            "super_status": data["optional_map"]["IS_SUPER"]["value"]["superStatus"],
            "user_registered": data["user_registered"],
        }
        return self._customer_info

    def _send_req(self, order_id: Optional[int]):
        param = {} if order_id is None else {"order_id": order_id}
        self._response = get(self._ourl, cookies=self._cookie_jar, params=param)
        self._resp_json = self._response.json()

    def _validate_response(self) -> None:
        self._response.raise_for_status()
        if not self._resp_json["statusCode"] == 0:
            raise HTTPError(f"Bad Response: {self._resp_json['statusMessage']}")

    def _parse_orders(self) -> list[dict]:
        self._validate_response()
        return [order for order in self._response.json()["data"]["orders"]]

    @property
    def _exhausted(self) -> bool:
        self._validate_response()
        return not bool(self._resp_json["data"]["orders"])

    def fetch(self, limit: Optional[int] = 20):
        limit = 10**8 if limit is None else limit
        if limit.__class__ is not int or limit < 0:
            raise ValueError(
                f"limit should be a positive integer, not {limit}({limit.__class__})"
            )
        if limit % 10 != 0:
            limit = round(limit, -1) + 10
            warn(f"Limit must be a multiple of 10. Fetching {limit} (max) orders.")
        self.orders_r = []
        self._send_req(order_id=None)
        self.orders_r.extend(self._parse_orders())
        while self._exhausted is False and len(self.orders_r) < limit:
            self._send_req(order_id=self.orders_r[-1]["order_id"])
            self.orders_r.extend(self._parse_orders())
            print(f"\r Retrieved {len(self.orders_r):>4} orders", end="")
        print(f"\r [Done] Retrieved {len(self.orders_r):>4} orders")
        self.orders_p = self._get_processed_order()
        self._fetched = True

    def fetchall(self):
        self.fetch(limit=None)

    def _get_processed_order(self):
        return [self._process_orders(deepcopy(order)) for order in self.orders_r]

    def _process_orders(self, order: dict):
        for ind, transaction in enumerate(order["payment_transactions"]):
            pg_response = transaction["paymentMeta"]["extPGResponse"]
            if pg_response.__class__ is str and pg_response != "":
                pg_response = pg_response.replace("false", "False")
                pg_response = pg_response.replace("true", "True")
                transaction["paymentMeta"]["extPGResponse"] = literal_eval(pg_response)
                order["payment_transactions"][ind] = transaction

        if order["offers_data"].__class__ is str and order["offers_data"] != "":
            order["offers_data"] = literal_eval(order["offers_data"])
        if order.get("rating_meta", None) is None:
            order["rating_meta"] = {
                "restaurant_rating": {"rating": 0},
                "delivery_rating": {"rating": 0},
            }
        else:
            order["rating_meta"].pop("asset_id", None)

        for attr in attrs["order"]:
            order.setdefault(attr, None)
        for attr in attrs["restaurant"]:
            order.setdefault(attr, None)
        for attr in attrs["delivery_address"]:
            order["delivery_address"].setdefault(attr, None)
        for attr in attrs["offers_data"]:
            for offer in order["offers_data"]:
                offer.setdefault(attr, None)
        for attr in attrs["payment"]:
            for payment in order["payment_transactions"]:
                payment.setdefault(attr, None)
        for attr in attrs["order_items"]:
            for item in order["order_items"]:
                item.setdefault(attr, None)
        return order

    def _order_by_id(self, obj, id, ver: Optional[int] = None):
        def _order():
            for order in self.orders_p:
                if order["order_id"] == id:
                    return order
            raise ValueError(f"order with id = {repr(id)} doesn't exist.")

        def _order_item():
            for order in self.orders_p:
                for item in order["order_items"]:
                    if item["item_id"] == id:
                        return order
            raise ValueError(f"order item with id = {repr(id)} doesn't exist.")

        def _restaurant():
            for order in self.orders_p:
                if order["restaurant_id"] == id:
                    return order
            raise ValueError(f"restaurant with id = {repr(id)} doesn't exist.")

        def _address():
            for order in self.orders_p:
                if (
                    self.ddav is True
                    and order["delivery_address"]["id"] == id
                    and order["delivery_address"]["version"] == ver
                ):
                    return order
                elif self.ddav is False and order["delivery_address"]["id"] == id:
                    return order
            raise ValueError(
                f"Address with (id,ver) = ({id},{ver}) doesn't exist."
            ) if self.ddav else ValueError(f"Address with id = {id} doesn't exist.")

        def _payment():
            for order in self.orders_p:
                if order["transactionId"] == id:
                    return order
            raise ValueError(f"payment with transaction id = {repr(id)} doesn't exist.")

        def _offer():
            for order in self.orders_p:
                for offer in order["offers_data"]:
                    if offer["id"] == id:
                        return order
            raise ValueError(f"delivery address with id = {repr(id)} doesn't exist.")

        obj_dict = {
            "order": _order,
            "item": _order_item,
            "restaurant": _restaurant,
            "address": _address,
            "payment": _payment,
            "offer": _offer,
        }
        return obj_dict[obj]()

    def order(self, id: Optional[int] = None):
        if id is None:
            return [convert.order(order, self.ddav) for order in self.orders_p]
        return convert.order(self._order_by_id("order", id), self.ddav)

    def orderitem(self, id: Optional[int] = None):
        if id is None:
            return list(
                chain.from_iterable(
                    [convert.orderitem(order) for order in self.orders_p]
                )
            )
        return convert.orderitem(self._order_by_id("item", id))

    def restaurant(self, id: Optional[int] = None):
        if id is None:
            return [convert.restaurant(order, self.ddav) for order in self.orders_p]
        return convert.restaurant(self._order_by_id("restaurant", id), self.ddav)

    def deliveryaddress(self, id: Optional[int] = None, ver: Optional[int] = None):
        if ver is not None and self.ddav is False:
            warn(f"version number will be ignored as bool ddav is False")
        if id is None:
            return [
                convert.deliveryaddress(order, self.ddav) for order in self.orders_p
            ]
        if ver is None and self.ddav is True:
            raise KeyError("provide version number of address as ddav is True")

        return convert.deliveryaddress(self._order_by_id("address", id, ver), self.ddav)

    def payment(self, id: Optional[int] = None):
        if id is None:
            return list(
                chain.from_iterable([convert.payment(order) for order in self.orders_p])
            )
        return convert.payment(self._order_by_id("payment", id))

    def offer(self, id: Optional[int] = None):
        if id is None:
            return list(
                chain.from_iterable([convert.offer(order) for order in self.orders_p])
            )
        return convert.offer(self._order_by_id("offer", id))

    def save(self, fname: str = "orders.json", **kwargs: dict):
        curr_ids = set(order["order_id"] for order in self.orders_r)
        try:
            with open("data/" + fname, "r", encoding="utf-8") as f:
                loaded = load(f)
                loaded_ids = set(order["order_id"] for order in loaded)
        except (JSONDecodeError, FileNotFoundError):
            with open("data/" + fname, "w", encoding="utf-8") as f:
                dump(self.orders_r, f, **kwargs)
        else:
            if diff := curr_ids.difference(loaded_ids):
                loaded.extend([i for i in self.orders_r if i["order_id"] in diff])
            with open("data/" + fname, "w", encoding="utf-8") as f:
                dump(loaded, f, **kwargs)

    def load(self, fname: str = "orders.json", **kwargs: dict):
        with open("data/" + fname, "r", encoding="utf-8") as f:
            self.orders_r = load(f, **kwargs)
        self.orders_p = self._get_processed_order()
        self._fetched = True

    def saveb(self, fname: str = "orders.msgpack", **kwargs: dict):
        curr_ids = set(order["order_id"] for order in self.orders_r)
        try:
            with open("data/" + fname, "rb") as f:
                loaded = unpack(f)
                loaded_ids = set(order["order_id"] for order in loaded)
        except (ValueError, FileNotFoundError):
            with open("data/" + fname, "wb") as f:
                pack(self.orders_r, f, **kwargs)
        else:
            if diff := curr_ids.difference(loaded_ids):
                loaded.extend([i for i in self.orders_r if i["order_id"] in diff])
            with open("data/" + fname, "wb") as f:
                pack(self.orders_r, f, **kwargs)

    def loadb(self, fname: str = "orders.msgpack", **kwargs: dict):
        with open("data/" + fname, "rb") as f:
            self.orders_r = unpack(f, **kwargs)
        self.orders_p = self._get_processed_order()
        self._fetched = True
