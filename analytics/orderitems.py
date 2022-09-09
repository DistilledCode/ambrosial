from collections import Counter, defaultdict
from itertools import chain
from typing import Optional, Union

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

    def _validate_id(self, item_id: str) -> bool:
        if item_id in [item.item_id for item in self.orderitems]:
            return True
        raise ValueError(f"order item of id = {repr(item_id)} does not exist.")

    def history(self, item_id: Optional[str] = None):
        hist = defaultdict(list)
        for item in self.orderitems:
            hist[item.item_id].append(
                {
                    "order_id": item.order_id,
                    "address_id": self.swiggy.order(item.order_id).delivery_address.id,
                    "order_time": self.swiggy.order(item.order_id).order_time,
                }
            )
        if item_id is not None:
            self._validate_id(item_id)
            return hist.get(item_id)
        return dict(hist)

    def summarise(self, item_id: str):
        self._validate_id(item_id)
        instances = [item for item in self.orderitems if item.item_id == item_id]
        qty = sum(i.quantity for i in instances)
        return {
            "tot_quantity": qty,
            "avg_base_price": round(sum(i.base_price for i in instances) / qty, 3),
            "tot_mrp": round(sum(i.subtotal for i in instances), 3),
            "tot_discount": round(sum(i.item_total_discount for i in instances), 3),
            "tot_actual_cost": round(sum(i.effective_item_price for i in instances), 3),
            "tot_tax": round(sum(sum(i.item_charges.values()) for i in instances), 3),
            "avg_actual_cost": round(
                sum(i.effective_item_price for i in instances) / qty, 3
            ),
            "image_url": instances[0].image,
            "received_for_free": {
                "quantity": sum(i.free_item_quantity for i in instances),
                "history": [
                    {
                        "order_id": item.order_id,
                        "address_id": self.swiggy.order(
                            item.order_id
                        ).delivery_address.id,
                        "order_time": self.swiggy.order(item.order_id).order_time,
                    }
                    for item in instances
                    if item.free_item_quantity > 0
                ],
            },
        }
