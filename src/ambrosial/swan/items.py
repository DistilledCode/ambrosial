from collections import Counter, defaultdict
from itertools import chain
from statistics import mean
from typing import Any, Optional

from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.item import Item


class ItemAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_items = self.swiggy.get_items()

    def group(self) -> dict[Item, int]:
        return dict(Counter(self.all_items).most_common())

    def group_by(self, attr: str) -> dict[str, int]:
        if attr == "item_charges":
            raise NotImplementedError("unhashable attribute type: <dict>")
        obj_dict = {
            "addons": self._get_addons_detail,
            "variants": self._get_variants_detail,
            "category_details": self._get_category_details,
        }

        if attr in obj_dict:
            return dict(obj_dict[attr]())
        return dict(self._get_attr_detail(attr))

    def history(self, item_id: Optional[int] = None) -> dict:
        hist = defaultdict(list)
        for item in self.all_items:
            hist[item.item_id].append(
                {
                    "order_id": item.order_id,
                    "address_id": self.swiggy.get_order(
                        item.order_id
                    ).address.address_id,
                    "order_time": self.swiggy.get_order(item.order_id).order_time,
                }
            )
        if item_id is not None and self._is_valid_id(item_id):
            return hist.get(item_id)  # type:ignore
        return dict(hist)

    def summarise(self, item_id: int) -> dict:
        self._is_valid_id(item_id)
        instances = [item for item in self.all_items if item.item_id == item_id]
        return {
            "total_quantity": sum(i.quantity for i in instances),
            "avg_base_price": round(mean(i.base_price for i in instances), 3),
            "total_mrp": round(sum(i.subtotal for i in instances), 3),
            "total_discount": round(sum(i.item_total_discount for i in instances), 3),
            "total_actual_cost": round(
                sum(i.effective_item_price for i in instances), 3
            ),
            "total_tax": round(sum(sum(i.item_charges.values()) for i in instances), 3),
            "avg_actual_cost": round(
                mean(i.effective_item_price for i in instances), 3
            ),
            "image_url": instances[0].image,
            "received_for_free": sum(i.free_item_quantity for i in instances),
        }

    def search_item(self, name: str, exact: bool = True) -> list[Item]:
        return (
            [item for item in self.all_items if name.lower() == item.name.lower()]
            if exact
            else [item for item in self.all_items if name.lower() in item.name.lower()]
        )

    def _is_valid_id(self, item_id: int) -> bool:
        if item_id in [item.item_id for item in self.all_items]:
            return True
        raise ValueError(f"order item of id = {repr(item_id)} does not exist.")

    def _get_attr_detail(self, attr: str) -> list[tuple[Any, int]]:
        return Counter(getattr(item, attr) for item in self.all_items).most_common()

    def _get_addons_detail(self) -> list[tuple[Any, int]]:
        return Counter(
            i["name"]
            for i in list(chain.from_iterable([item.addons for item in self.all_items]))
        ).most_common()

    def _get_variants_detail(self) -> list[tuple[Any, int]]:
        return Counter(
            i["name"]
            for i in list(
                chain.from_iterable([item.variants for item in self.all_items])
            )
        ).most_common()

    def _get_category_details(self) -> list[tuple[str, int]]:
        return Counter(
            item.category_details["category"] for item in self.all_items
        ).most_common()
