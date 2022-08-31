from ast import literal_eval
from functools import cache
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
        self.orders_raw = []
        self.orders_processed = []
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
            warn(f"Orders are fetched in multiples of 10. Fetching {(limit//10+1)*10}.")
        self.orders_raw = []
        self._send_req(order_id=None)
        self.orders_raw.extend(self._parse_orders())
        while self._exhausted is False and len(self.orders_raw) < limit:
            self._send_req(order_id=self.orders_raw[-1]["order_id"])
            self.orders_raw.extend(self._parse_orders())
            print(f"\r Retrieved {len(self.orders_raw):>4} orders", end="")
        print()
        self.orders_processed = [self._post_process(order) for order in self.orders_raw]

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
        for attr in attrs["order"] + attrs["restaurant"] + attrs["delivery_address"]:
            order.setdefault(attr, None)
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

    @cache
    def order_by_id(self, order_id: int, dclass: bool = True) -> dict:
        for order_ in self.orders_processed:
            if order_["order_id"] == order_id:
                return self.order(order_) if dclass else order_
        return dict()

    def order(self, order_id: Optional[int] = None):
        if order_id is None:
            return [convert.order(order) for order in self.orders_processed]
        return convert.order(self.order_by_id(order_id))

    def orderitem(self, order_id: Optional[int] = None):
        if order_id is None:
            return list(
                chain.from_iterable(
                    [convert.orderitem(order) for order in self.orders_processed]
                )
            )
        return convert.orderitem(self.order_by_id(order_id))

    def restaurant(self, order_id: Optional[int] = None):
        if order_id is None:
            return [convert.restaurant(order) for order in self.orders_processed]
        return convert.restaurant(self.order_by_id(order_id))

    def deliveryaddress(self, order_id: Optional[int] = None):
        if order_id is None:
            return [convert.deliveryaddress(order) for order in self.orders_processed]
        return convert.deliveryaddress(self.order_by_id(order_id))

    def payment(self, order_id: Optional[int] = None):
        if order_id is None:
            return list(
                chain.from_iterable(
                    [convert.payment(order) for order in self.orders_processed]
                )
            )
        return convert.payment(self.order_by_id(order_id))

    def offer(self, order_id: Optional[int] = None):
        if order_id is None:
            return list(
                chain.from_iterable(
                    [convert.offers_data(order) for order in self.orders_processed]
                )
            )
        return convert.offers_data(self.order_by_id(order_id))

    def save(self, fname: str = "orders.json", **kwargs: dict):
        obj = {"raw": self.orders_raw, "processed": self.orders_processed}
        with open(fname, "w", encoding="utf-8") as f:
            dump(obj, f, **kwargs)

    def load(self, fname: str = "orders.json", **kwargs: dict):
        with open(fname, "r", encoding="utf-8") as f:
            obj = load(f, **kwargs)
        self.orders_raw = obj["raw"]
        self.orders_processed = obj["processed"]

    def saveb(self, fname: str = "orders.msgpack", **kwargs: dict):
        obj = {"raw": self.orders_raw, "processes": self.orders_processed}
        with open(fname, "wb") as f:
            pack(obj, f, **kwargs)

    def loadb(self, fname: str = "orders.msgpack", **kwargs: dict):
        with open(fname, "rb") as f:
            obj = unpack(f, **kwargs)
        self.orders_raw = obj["raw"]
        self.orders_processed = obj["processed"]
