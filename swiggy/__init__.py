from ast import literal_eval
from copy import deepcopy
from itertools import chain
from json import dump, load
from typing import Optional
from warnings import warn

import browser_cookie3
from msgpack import pack, unpack
from requests import get

import swiggy.convert as convert
from swiggy.convert import attrs


class Swiggy:
    def __init__(self):
        self.url = "https://www.swiggy.com/dapi/order/all"
        self.cookie_jar = browser_cookie3.load("www.swiggy.com")
        self.orders_r = []
        self.orders_p = []
        self.json = ""
        self.response = None
        self.reason = ""

    def _send_req(self, order_id: Optional[int]):
        param = {} if order_id is None else {"order_id": order_id}
        self.response = get(self.url, cookies=self.cookie_jar, params=param)
        self.json = self.response.json()

    def _valid_response(self) -> bool:
        if not self.response.status_code == 200:
            self.reason = self.response.reason
            return False
        if not self.json["statusCode"] == 0:
            self.reason = self.json["statusMessage"]
            return False
        self.reason = None
        return True

    def _parse_orders(self) -> list[dict]:
        if not self._valid_response():
            print(self.reason)
            quit()
        return [order for order in self.response.json()["data"]["orders"]]

    @property
    def _exhausted(self) -> bool:
        if not self._valid_response():
            print(self.reason)
            quit()
        return not bool(self.json["data"]["orders"])

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
        print()
        self.orders_p = [self._post_process(deepcopy(order)) for order in self.orders_r]

    def fetchall(self):
        self.fetch(limit=None)

    def _post_process(self, order: dict):
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

    def _order_by_id(self, obj, id):
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
                if order["delivery_address"]["id"] == id:
                    return order
            raise ValueError(f"delivery address with id = {repr(id)} doesn't exist.")

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
            return [convert.order(order) for order in self.orders_p]
        return convert.order(self._order_by_id("order", id))

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
            return [convert.restaurant(order) for order in self.orders_p]
        return convert.restaurant(self._order_by_id("restaurant", id))

    def deliveryaddress(self, id: Optional[int] = None):
        if id is None:
            return [convert.deliveryaddress(order) for order in self.orders_p]
        return convert.deliveryaddress(self._order_by_id("address", id))

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
        obj = {"raw": self.orders_r, "processed": self.orders_p}
        with open(fname, "w", encoding="utf-8") as f:
            dump(obj, f, **kwargs)

    def load(self, fname: str = "orders.json", **kwargs: dict):
        with open(fname, "r", encoding="utf-8") as f:
            obj = load(f, **kwargs)
        self.orders_r = obj["raw"]
        self.orders_p = obj["processed"]

    def saveb(self, fname: str = "orders.msgpack", **kwargs: dict):
        obj = {"raw": self.orders_r, "processed": self.orders_p}
        with open(fname, "wb") as f:
            pack(obj, f, **kwargs)

    def loadb(self, fname: str = "orders.msgpack", **kwargs: dict):
        with open(fname, "rb") as f:
            obj = unpack(f, **kwargs)
        self.orders_r = obj["raw"]
        self.orders_p = obj["processed"]
