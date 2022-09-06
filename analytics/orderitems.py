from collections import Counter
from itertools import chain
from typing import Union

from swiggy import Swiggy
from swiggy.orderitem import OrderItem

from analytics import SwiggyAnalytics


class OrderitemAnalytics(SwiggyAnalytics):
    def __init__(self, swiggy: Swiggy = None) -> None:
        SwiggyAnalytics.__init__(self, swiggy)

    def most_common(self, attr: str = None) -> dict[Union[OrderItem, str], int]:
        if attr is None:
            return dict(Counter(self.orderitems).most_common())
        if attr == "item_charges":
            raise NotImplementedError("not compatible with unhashable attribute types")
        if attr == "category_details":
            return dict(
                Counter(
                    getattr(i, attr)["category"] for i in self.orderitems
                ).most_common()
            )
        if attr in ["addons", "variants"]:
            return dict(
                Counter(
                    i["name"]
                    for i in list(
                        chain.from_iterable([getattr(i, attr) for i in self.orderitems])
                    )
                ).most_common()
            )
        return dict(Counter(getattr(i, attr) for i in self.orderitems).most_common())
