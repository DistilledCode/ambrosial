from collections import Counter, defaultdict
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

    def history(self, reverse: bool = False):
        hist = defaultdict(list)
        for order in self.orders:
            for item in order.order_items:
                hist[item.item_id].append(
                    {
                        "order_id": order.order_id,
                        "address_id": order.delivery_address.id,
                        "order_time": order.order_time,
                    }
                )
        if reverse is True:
            for key in hist:
                hist[key].sort()
        return dict(hist)

    def summarise(self, item_id: str):
        if item_id not in [i.item_id for i in self.orderitems]:
            raise ValueError(f"order item of id = {repr(id)} does not exist.")
        summary = dict()
        instances = [item for item in self.orderitems if item.item_id == item_id]
        summary["total_quantity"] = sum(i.quantity for i in instances)
        summary["image_url"] = instances[0].image
        summary["total_tax"] = sum(sum(i.item_charges.values()) for i in instances)
        summary["total_mrp"] = sum(i.subtotal for i in instances)
        summary["total_discount"] = sum(i.item_total_discount for i in instances)
        summary["total_actual_cost"] = sum(i.effective_item_price for i in instances)
        summary["avg_actual_cost"] = (
            summary["total_actual_cost"] / summary["total_quantity"]
        )
        summary["order_history"] = self.history().get(item_id)
        summary["received_for_free"] = {
            "quantity": sum(i.free_item_quantity for i in instances),
            "history": [
                {
                    "order_id": item.order_id,
                    "address_id": self.swiggy.order(item.order_id).delivery_address.id,
                    "order_time": self.swiggy.order(item.order_id).order_time,
                }
                for item in instances
                if item.free_item_quantity > 0
            ],
        }
        return summary
