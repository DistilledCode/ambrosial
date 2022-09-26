from ast import literal_eval
from copy import deepcopy
from itertools import chain
from json import JSONDecodeError, dump, load
from pathlib import Path
from typing import Any, Optional
from warnings import warn

import browser_cookie3
from msgpack import pack, unpack
from requests import HTTPError, get

import ambrosial.swiggy.convert as convert
from ambrosial.swiggy.address import Address
from ambrosial.swiggy.item import Item
from ambrosial.swiggy.order import Offer, Order, Payment
from ambrosial.swiggy.restaurant import Restaurant
from ambrosial.swiggy.utils import find_order


class Swiggy:
    def __init__(self, ddav: bool = False) -> None:
        self.ddav = ddav
        self._o_url = "https://www.swiggy.com/dapi/order/all"
        self._p_url = "https://www.swiggy.com/mapi/profile/info"
        self._cookie_jar = browser_cookie3.load("www.swiggy.com")
        self.orders_raw: list[dict[str, Any]] = []
        self.orders_refined: list[dict[str, Any]] = []
        self._resp_json: dict = {}
        self._invalid_reason = ""
        self._customer_info: dict = {}
        self._fetched = False
        self._save_path: Path = Path(__file__).resolve().parents[3] / "data"
        self._create_save_path()

    @property
    def _is_exhausted(self) -> bool:
        self._validate_response()
        return not bool(self._resp_json["data"]["orders"])

    def get_account_info(self) -> dict:
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

    def fetch_orders(self) -> None:
        self.orders_raw = []
        self._send_req(order_id=None)
        self.orders_raw.extend(self._parse_orders())
        print("Retrieving orders...")
        while self._is_exhausted is False:
            self._send_req(order_id=self.orders_raw[-1]["order_id"])
            self.orders_raw.extend(self._parse_orders())
        print(f"Retrieved {len(self.orders_raw):>4} orders")
        self.orders_refined = self._get_processed_order()
        self._fetched = True

    def fetchall(self) -> None:
        self.fetch_orders()
        self.get_account_info()

    def get_order(self, id_: int) -> Order:
        return convert.order(find_order("order", self.orders_refined, id_), self.ddav)

    def get_orders(self) -> list[Order]:
        return [convert.order(order, self.ddav) for order in self.orders_refined]

    def get_item(self, id_: int) -> list[Item]:
        return convert.item(find_order("item", self.orders_refined, id_))

    def get_items(self) -> list[Item]:
        return list(
            chain.from_iterable([convert.item(order) for order in self.orders_refined])
        )

    def get_restaurant(self, id_: int) -> Restaurant:
        return convert.restaurant(
            find_order("restaurant", self.orders_refined, id_), self.ddav
        )

    def get_restaurants(self) -> list[Restaurant]:
        return [convert.restaurant(order, self.ddav) for order in self.orders_refined]

    def get_address(self, id_: int, ver: Optional[int] = None) -> Address:
        if ver is not None and self.ddav is False:
            warn("version number will be ignored as ddav is False")
        if ver is None and self.ddav is True:
            raise KeyError("provide version number of address as ddav is True")
        order_ = find_order(
            "address",
            self.orders_refined,
            id_,
            kwarg={"ver": ver, "ddav": self.ddav},
        )
        return convert.address(order_, self.ddav)

    def get_addresses(self) -> list[Address]:
        return [convert.address(order, self.ddav) for order in self.orders_refined]

    def get_offer(self, id_: int) -> list[Offer]:
        return convert.offer(find_order("offer", self.orders_refined, id_))

    def get_offers(self) -> list[Offer]:
        return list(
            chain.from_iterable([convert.offer(order) for order in self.orders_refined])
        )

    def get_payment(self, id_: int) -> list[Payment]:
        return convert.payment(find_order("payment", self.orders_refined, id_))

    def get_payments(self) -> list[Payment]:
        return list(
            chain.from_iterable(
                [convert.payment(order) for order in self.orders_refined]
            )
        )

    def save(self, fname: str = "orders.json") -> None:
        curr_ids = {order["order_id"] for order in self.orders_raw}
        try:
            with open(self._save_path / fname, "r", encoding="utf-8") as f:
                loaded = load(f)
                loaded_ids = {order["order_id"] for order in loaded}
        except (JSONDecodeError, FileNotFoundError):
            with open(self._save_path / fname, "w", encoding="utf-8") as f:
                dump(self.orders_raw, f, indent=4)
        else:
            if diff := curr_ids.difference(loaded_ids):
                loaded.extend([i for i in self.orders_raw if i["order_id"] in diff])
            with open(self._save_path / fname, "w", encoding="utf-8") as f:
                dump(loaded, f, indent=4)

    def load(self, fname: str = "orders.json") -> None:
        with open(self._save_path / fname, "r", encoding="utf-8") as f:
            self.orders_raw = load(f)
        self.orders_refined = self._get_processed_order()
        self._fetched = True

    def saveb(self, fname: str = "orders.msgpack") -> None:
        curr_ids = {order["order_id"] for order in self.orders_raw}
        try:
            with open(self._save_path / fname, "rb") as f:
                loaded = unpack(f)
                loaded_ids = {order["order_id"] for order in loaded}
        except (ValueError, FileNotFoundError):
            with open(self._save_path / fname, "wb") as f:
                pack(self.orders_raw, f)
        else:
            if diff := curr_ids.difference(loaded_ids):
                loaded.extend([i for i in self.orders_raw if i["order_id"] in diff])
            with open(self._save_path / fname, "wb") as f:
                pack(self.orders_raw, f)

    def loadb(self, fname: str = "orders.msgpack") -> None:
        with open(self._save_path / fname, "rb") as f:
            self.orders_raw = unpack(f)
        self.orders_refined = self._get_processed_order()
        self._fetched = True

    def _create_save_path(self) -> None:
        if self._save_path.exists() is False:
            self._save_path.mkdir(parents=True, exist_ok=True)

    def _send_req(self, order_id: Optional[int]) -> None:
        param = {} if order_id is None else {"order_id": order_id}
        self._response = get(self._o_url, cookies=self._cookie_jar, params=param)
        self._resp_json = self._response.json()

    def _get_processed_order(self) -> list[dict]:
        return [self._process_orders(deepcopy(order)) for order in self.orders_raw]

    def _fix_payment(self, order: dict) -> dict:
        for ind, transaction in enumerate(order["payment_transactions"]):
            pg_response = transaction["paymentMeta"]["extPGResponse"]
            if pg_response.__class__ is str and pg_response != "":
                pg_response = pg_response.replace("false", "False")
                pg_response = pg_response.replace("true", "True")
                transaction["paymentMeta"]["extPGResponse"] = literal_eval(pg_response)
                order["payment_transactions"][ind] = transaction
        return order

    def _process_orders(self, order: dict) -> dict:
        order = self._fix_payment(order)
        if order["offers_data"].__class__ is str and order["offers_data"] != "":
            order["offers_data"] = literal_eval(order["offers_data"])
        if order.get("rating_meta", None) is None:
            order["rating_meta"] = {
                "restaurant_rating": {"rating": 0},
                "delivery_rating": {"rating": 0},
            }
        else:
            order["rating_meta"].pop("asset_id", None)
        return order

    def _validate_response(self) -> None:
        self._response.raise_for_status()
        if not self._resp_json["statusCode"] == 0:
            raise HTTPError(f"Bad Response: {self._resp_json['statusMessage']}")

    def _parse_orders(self) -> list[dict]:
        self._validate_response()
        return self._response.json()["data"]["orders"]

    def __repr__(self) -> str:
        return f"Swiggy(ddav = {self.ddav})"
