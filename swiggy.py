from ast import literal_eval
from json import dump, load
from typing import Optional

import browser_cookie3
from msgpack import pack, unpack
from requests import get

from utils import dict2dataclass


class Swiggy:
    def __init__(self):
        self.url = "https://www.swiggy.com/dapi/order/all"
        self.cookie_jar = browser_cookie3.load("www.swiggy.com")
        self.orders = []

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

    def as_dataclass(self):
        self.orders_ = [
            dict2dataclass(f"order{index}", order)
            for index, order in enumerate(self.orders)
        ]

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
        self._send_req(order_id=None)
        self.orders.extend(self._parse_orders())
        while self._exhausted is False and len(self.orders) < limit:
            self._send_req(order_id=self.orders[-1]["order_id"])
            self.orders.extend(self._parse_orders())
            print(f"\r Retrieved {min(len(self.orders),limit):>4} orders", end="")
        print()
        self.orders = [self._evaluate(order) for order in self.orders][:limit]

    def fetchall(self):
        self.fetch(limit=None)

    def _evaluate(self, order: dict):
        for ind, transaction in enumerate(order["payment_transactions"]):
            pg_response = transaction["paymentMeta"]["extPGResponse"]
            if pg_response.__class__ is str and pg_response != "":
                pg_response = pg_response.replace("false", "False")
                pg_response = pg_response.replace("true", "True")
                transaction["paymentMeta"]["extPGResponse"] = literal_eval(pg_response)
                order["payment_transactions"][ind] = transaction
        order["paymentTransactions"] = order["payment_transactions"]

        if order["offers_data"].__class__ is str and order["offers_data"] != "":
            order["offers_data"] = literal_eval(order["offers_data"])
        return order

    def save(self, fname: str = "orders.json", **kwargs: dict):
        with open(fname, "w", encoding="utf-8") as f:
            dump(self.orders, f, **kwargs)

    def load(self, fname: str = "orders.json", **kwargs: dict):
        with open(fname, "r", encoding="utf-8") as f:
            self.orders = load(f, **kwargs)

    def saveb(self, fname: str = "orders.msgpack", **kwargs: dict):
        with open(fname, "wb") as f:
            pack(self.orders, f, **kwargs)

    def loadb(self, fname: str = "orders.msgpack", **kwargs: dict):
        with open(fname, "rb") as f:
            self.orders = unpack(f, **kwargs)
