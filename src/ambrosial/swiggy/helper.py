from collections import defaultdict
from typing import TypeAlias

from ambrosial.swiggy.utils import SwiggyOrderDict

OrderId: TypeAlias = int


class Cache:
    def __init__(self, orders_refined: list[SwiggyOrderDict]) -> None:
        self.orders_refined = orders_refined
        self.orders: dict[OrderId, SwiggyOrderDict] = {}
        self.items: dict[str, list[OrderId]] = defaultdict(list)
        self.resturants: dict[str, list[OrderId]] = defaultdict(list)
        self.addresses: dict[str, list[OrderId]] = defaultdict(list)
        self.addresses_ver: dict[str, list[OrderId]] = defaultdict(list)
        self.payment: dict[str, list[OrderId]] = defaultdict(list)
        self.cache()

    def cache(self) -> None:
        for order in self.orders_refined:
            order_id = order["order_id"]
            self.orders[order_id] = order
            for item in order["order_items"]:
                self.items[item["item_id"]].append(order_id)
            self.resturants[order["restaurant_id"]].append(order_id)
            self.addresses[order["delivery_address"]["id"]].append(order_id)
            address_w_ver = (
                f'{order["delivery_address"]["id"]}_'
                f'{order["delivery_address"]["version"]}'
            )
            self.addresses_ver[address_w_ver].append(order_id)
            for transaction in order["payment_transactions"]:
                self.payment[transaction["transactionId"]].append(order_id)

    def get_order(self, order_id: int) -> SwiggyOrderDict:
        if (x := self.orders.get(order_id, None)) is not None:
            return x
        raise ValueError(f"order_id {repr(order_id)}{type(order_id)} doesn't exist.")

    def get_item(self, item_id: str) -> SwiggyOrderDict:
        if (x := self.items.get(item_id, None)) is not None:
            return self.get_order(order_id=x[0])
        raise ValueError(f"item_id {repr(item_id)}{type(item_id)} doesn't exist.")

    def get_restaurant(self, restaurant_id: str) -> SwiggyOrderDict:
        if (x := self.resturants.get(restaurant_id, None)) is not None:
            return self.get_order(order_id=x[0])
        raise ValueError(
            f"restaurant_id {repr(restaurant_id)}{type(restaurant_id)} doesn't exist."
        )

    def get_address(self, address_id: str) -> SwiggyOrderDict:
        if (x := self.addresses.get(address_id, None)) is not None:
            return self.get_order(order_id=x[0])
        raise ValueError(
            f"address_id {repr(address_id)}{type(address_id)} doesn't exist."
        )

    def get_address_w_ver(self, address_id: str, ver: int) -> SwiggyOrderDict:
        address_id = f"{address_id}_{ver}"
        if (x := self.addresses_ver.get(address_id, None)) is not None:
            return self.get_order(order_id=x[0])
        raise ValueError(
            f"address_id,version_id {repr(address_id)}{type(address_id)},"
            f"{repr(ver)}{type(ver)} doesn't exist."
        )

    def get_offer(self, order_id: int) -> SwiggyOrderDict:
        return self.get_order(order_id=order_id)

    def get_payment(self, transaction_id: str) -> SwiggyOrderDict:
        if (x := self.payment.get(transaction_id, None)) is not None:
            return self.get_order(order_id=x[0])
        raise ValueError(
            f"payment_id {repr(transaction_id)}{type(transaction_id)} doesn't exist."
        )
