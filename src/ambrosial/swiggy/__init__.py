from copy import deepcopy
from itertools import chain
from pathlib import Path
from typing import Any, Optional
from warnings import warn

from requests import Response, get

import ambrosial.swiggy.convert as convert
import ambrosial.swiggy.iohandler as ioh
import ambrosial.swiggy.utils as utils
from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.order import Offer, Order, Payment
from ambrosial.swiggy.datamodel.restaurant import Restaurant
from ambrosial.swiggy.helper import find_order
from ambrosial.swiggy.utils import SwiggyOrderDict


class Swiggy:
    def __init__(self, path: Optional[Path] = None, ddav: bool = False) -> None:
        self.ddav = ddav
        self._o_url = "https://www.swiggy.com/dapi/order/all"
        self._p_url = "https://www.swiggy.com/mapi/profile/info"
        self.orders_raw: list[SwiggyOrderDict] = []
        self.orders_refined: list[SwiggyOrderDict] = []
        self._response: Response = Response()
        self._response_json: dict[str, Any] = {}
        self._customer_info: utils.UserInfo = {}
        self._fetched = False
        self.home_path = Path.home() / ".ambrosial" if path is None else path
        self._data_path = self.home_path / "data"
        self._cookie_jar = utils.get_cookies("www.swiggy.com")
        utils.create_path(self._data_path)

    @property
    def _is_exhausted(self) -> bool:
        utils.validate_response(self._response)
        return not bool(self._response_json["data"]["orders"])

    def get_account_info(self) -> utils.UserInfo:
        if self._customer_info is not None:
            return self._customer_info
        temp_cookie = self._cookie_jar
        temp_cookie.set_cookie(utils.get_empty_sid())
        self._response = get(self._p_url, cookies=temp_cookie)
        self._response_json = self._response.json()
        utils.validate_response(self._response)
        data = self._response_json["data"]
        self._customer_info = utils.UserInfo(
            customer_id=data["customer_id"],
            name=data["name"],
            mobile=data["mobile"],
            email=data["email"],
            emailVerified=data["emailVerified"],
            super_status=data["optional_map"]["IS_SUPER"]["value"]["superStatus"],
            user_registered=data["user_registered"],
        )
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
        return convert.order(
            find_order(
                "order",
                self.orders_refined,
                id_,
            ),
            self.ddav,
        )

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
            find_order(
                "restaurant",
                self.orders_refined,
                id_,
            ),
            self.ddav,
        )

    def get_restaurants(self) -> list[Restaurant]:
        return [convert.restaurant(order, self.ddav) for order in self.orders_refined]

    def get_address(self, id_: int, ver: Optional[int] = None) -> Address:
        if ver is not None and self.ddav is False:
            warn(f"version number will be ignored as {self.ddav=}")
        if ver is None and self.ddav is True:
            raise KeyError(f"provide version number of address as {self.ddav=}")
        order_ = find_order(
            "address",
            self.orders_refined,
            id_,
            ver=ver,
            ddav=self.ddav,
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

    def savej(self, fname: str = "orders.json") -> None:
        ioh.savej(self._data_path / fname, self.orders_raw)

    def saveb(self, fname: str = "orders.msgpack") -> None:
        ioh.saveb(self._data_path / fname, self.orders_raw)

    def loadj(self, fname: str = "orders.json") -> None:
        self.orders_raw = ioh.loadj(self._data_path / fname)
        self.orders_refined = self._get_processed_order()
        self._fetched = True

    def loadb(self, fname: str = "orders.msgpack") -> None:
        self.orders_raw = ioh.loadb(self._data_path / fname)
        self.orders_refined = self._get_processed_order()
        self._fetched = True

    def _send_req(self, order_id: Optional[int] = None) -> None:
        param = {} if order_id is None else {"order_id": order_id}
        self._response = get(self._o_url, cookies=self._cookie_jar, params=param)
        self._response_json = self._response.json()

    def _get_processed_order(self) -> list[SwiggyOrderDict]:
        return [utils.process_orders(deepcopy(order)) for order in self.orders_raw]

    def _parse_orders(self) -> list[SwiggyOrderDict]:
        utils.validate_response(self._response)
        return self._response.json()["data"]["orders"]

    def __repr__(self) -> str:
        return f"Swiggy(ddav = {self.ddav})"
