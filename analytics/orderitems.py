from collections import Counter
from typing import Union

from swiggy import Swiggy
from swiggy.orderitem import OrderItem

from analytics import SwiggyAnalytics


class OrderitemAnalytics(SwiggyAnalytics):
    def __init__(self, swiggy: Swiggy = None) -> None:
        SwiggyAnalytics.__init__(self, swiggy)
        # self.counter = Counter(self.orderitems)

    def most_common(self, attr: str = None) -> dict[Union[OrderItem, str], int]:
        if attr is None:
            return dict(Counter(self.orderitems).most_common())
        if attr in ["variants", "addons", "item_charges"]:
            raise NotImplementedError("not compatible with unhashable attribute types")
        if attr == "category_details":
            return dict(
                Counter(
                    getattr(i, attr)["category"] for i in self.orderitems
                ).most_common()
            )
        return dict(Counter(getattr(i, attr) for i in self.orderitems).most_common())
