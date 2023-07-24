from copy import deepcopy
from pathlib import Path
from typing import Any, ClassVar, Optional
from warnings import warn

from requests import Response, get

import ambrosial.swiggy.convert as convert
import ambrosial.swiggy.iohandler as ioh
import ambrosial.swiggy.utils as utils
from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.order import Offer, Order, Payment
from ambrosial.swiggy.datamodel.restaurant import Restaurant
from ambrosial.swiggy.helper import Cache
from ambrosial.swiggy.utils import SwiggyOrderDict


class Swiggy:
    order_url: ClassVar[str] = "https://www.swiggy.com/dapi/order/all"
    profile_url: ClassVar[str] = "https://www.swiggy.com/mapi/profile/info"

    def __init__(self, path: Optional[Path] = None, ddav: bool = False) -> None:
        self.ddav = ddav
        self.orders_raw: list[SwiggyOrderDict] = []
        self.orders_refined: list[SwiggyOrderDict] = []
        self._response: Response = Response()
        self._response_json: dict[str, Any] = {}
        self._fetched = False
        self.home_path = Path.home() / ".ambrosial" if path is None else path
        self._data_path = self.home_path / "data"
        self._cookie_jar = utils.get_cookies("www.swiggy.com")
        utils.create_path(self._data_path)

    @property
    def _is_exhausted(self) -> bool:
        utils.validate_response(self._response)
        return not bool(self._response_json["data"]["orders"])

    # def get_account_info(self) -> utils.UserInfo:
    #     temp_cookie = self._cookie_jar
    #     temp_cookie.set_cookie(utils.get_empty_sid())
    #     self._response = get(Swiggy.profile_url, cookies=temp_cookie)
    #     self._response_json = self._response.json()
    #     utils.validate_response(self._response)
    #     data = self._response_json["data"]
    #     return utils.UserInfo(
    #         customer_id=data["customer_id"],
    #         name=data["name"],
    #         mobile=data["mobile"],
    #         email=data["email"],
    #         emailVerified=data["emailVerified"],
    #         super_status=data["optional_map"]["IS_SUPER"]["value"]["superStatus"],
    #         user_registered=data["user_registered"],
    #     )

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
        self._post_fetch()

    # def fetchall(self) -> None:
    #     """Fetch both order details & account info.

    #     Same as calling ``fetch_orders()`` and ``get_account_info()``.
    #     """
    #     self.fetch_orders()
    #     self.get_account_info()

    def get_order(self, order_id: int) -> Order:
        return convert.order(self.cache.get_order(order_id=order_id), self.ddav)

    def get_orders(self) -> list[Order]:
        return [convert.order(order, self.ddav) for order in self.orders_refined]

    def get_item(self, item_id: int) -> Item:
        # convert.item() returns all the order items of the first order that contains
        # an item having `item_id`. If not, cache.get_item() raised ValueError.
        # Thus, the comprehension is guaranteed to contain an Item with given item_id.
        return [
            item
            for item in convert.item(self.cache.get_item(item_id=str(item_id)))
            if item.item_id == item_id
        ][0]

    def get_items(self) -> list[Item]:
        return [item for order in self.orders_refined for item in convert.item(order)]

    def get_restaurant(self, restaurant_id: int) -> Restaurant:
        return convert.restaurant(
            self.cache.get_restaurant(restaurant_id=str(restaurant_id)),
            self.ddav,
        )

    def get_restaurants(self) -> list[Restaurant]:
        return [convert.restaurant(order, self.ddav) for order in self.orders_refined]

    def get_address(self, address_id: int, ver: Optional[int] = None) -> Address:
        if self.ddav is False and ver is not None:
            warn(f"version number will be ignored as {self.ddav=}")
            order = self.cache.get_address(address_id=str(address_id))
        if self.ddav is True and ver is None:
            raise KeyError(f"provide version number of address as {self.ddav=}")
        if self.ddav is True and ver is not None:
            order = self.cache.get_address_w_ver(
                address_id=str(address_id),
                ver=int(ver),
            )
        return convert.address(order, self.ddav)

    def get_addresses(self) -> list[Address]:
        return [convert.address(order, self.ddav) for order in self.orders_refined]

    def get_offer(self, order_id: int) -> list[Offer]:
        return convert.offer(self.cache.get_offer(order_id=int(order_id)))

    def get_offers(self) -> list[Offer]:
        return [
            offer for order in self.orders_refined for offer in convert.offer(order)
        ]

    def get_payment(self, transaction_id: int) -> list[Payment]:
        return convert.payment(
            self.cache.get_payment(transaction_id=str(transaction_id))
        )

    def get_payments(self) -> list[Payment]:
        return [
            payment
            for order in self.orders_refined
            for payment in convert.payment(order)
        ]

    def savej(self, fname: str = "orders.json") -> None:
        ioh.savej(self._data_path / fname, self.orders_raw)

    def saveb(self, fname: str = "orders.msgpack") -> None:
        ioh.saveb(self._data_path / fname, self.orders_raw)

    def loadj(self, fname: str = "orders.json") -> None:
        self.orders_raw = ioh.loadj(self._data_path / fname)
        self.orders_refined = self._get_processed_order()
        self._post_fetch()

    def loadb(self, fname: str = "orders.msgpack") -> None:
        self.orders_raw = ioh.loadb(self._data_path / fname)
        self.orders_refined = self._get_processed_order()
        self._post_fetch()

    def _send_req(self, order_id: Optional[int] = None) -> None:
        param = {} if order_id is None else {"order_id": order_id}
        cookie_str = "; ".join([f"{c.name}={c.value}" for c in self._cookie_jar])

        headers_list = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.swiggy.com/my-account",
            "Content-Type": "application/json",
            "__fetch_req__": "true",
            "Connection": "keep-alive",
            "Cookie": cookie_str,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        self._response = get(Swiggy.order_url, headers=headers_list, params=param)
        self._response_json = self._response.json()

    def _get_processed_order(self) -> list[SwiggyOrderDict]:
        return [utils.process_orders(deepcopy(order)) for order in self.orders_raw]

    def _parse_orders(self) -> list[SwiggyOrderDict]:
        utils.validate_response(self._response)
        return self._response.json()["data"]["orders"]

    def _post_fetch(self) -> None:
        self._fetched = True
        self.cache: Cache = Cache(self.orders_refined)

    def __repr__(self) -> str:
        return f"Swiggy(ddav = {self.ddav})"
