from collections import Counter, defaultdict
from itertools import groupby
from typing import Any, Optional

import ambrosial.swan.typealiases as alias
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.item import Item


class ItemAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_items = self.swiggy.get_items()
        self.items_map = self._get_items_map()

    def group(self) -> dict[Item, int]:
        return dict(Counter(self.all_items).most_common())

    def group_by(self, attr: str) -> dict[Any, int]:
        if attr == "item_charges":
            raise NotImplementedError("unhashable type: 'dict'")
        obj_dict = {
            "addons": self._get_addons_detail,
            "variants": self._get_variants_detail,
            "category_details": self._get_category_details,
        }

        if attr in obj_dict:
            return dict(obj_dict[attr]())
        return dict(self._get_attr_detail(attr))

    def grouped_instances(self, key: str, attr: Optional[str] = None) -> dict[Any, Any]:
        g_dict = defaultdict(list)
        for item in self.all_items:
            if attr is None:
                g_dict[getattr(item, key)].append(item)
            else:
                g_dict[getattr(item, key)].append(getattr(item, attr))
        return dict(g_dict)

    def history(
        self,
        item_id: Optional[int] = None,
    ) -> dict[int, list[alias.History]]:
        if item_id is not None and self._is_valid_id(item_id):
            item_map = {item_id: self.items_map[item_id]}
        else:
            item_map = self.items_map
        return {
            item_id: [
                alias.History(
                    order_id=item.order_id,
                    address_id=self.swiggy.get_order(item.order_id).address.address_id,
                    order_time=self.swiggy.get_order(item.order_id).order_time,
                )
                for item in items
            ]
            for item_id, items in item_map.items()
        }

    def summarise(self, item_id: int) -> alias.Summarise:
        """
        total_actual_cost & avg_actual_cost inlcudes GST but excludes
        Packaging, Convenience, Cancellation, and Delivery Charges.
        Those are calculated for each order.
        """
        self._is_valid_id(item_id)
        instances = self.items_map[item_id]
        total_quantity = 0
        total_base_price = 0.0
        total_base_price = 0.0
        total_discount = 0.0
        total_actual_cost = 0.0
        total_tax = 0.0
        received_for_free = 0
        for item in instances:
            total_quantity += item.quantity - item.free_item_quantity
            total_base_price += item.subtotal
            total_discount += item.item_total_discount
            total_actual_cost += item.effective_item_price
            total_tax += sum(item.item_charges.values())
            received_for_free += item.free_item_quantity
        return alias.Summarise(
            total_quantity=total_quantity,
            avg_base_price=round(total_base_price / total_quantity, 3),
            total_base_price=round(total_base_price, 3),
            total_discount=round(total_discount, 3),
            total_actual_cost=round(total_actual_cost, 3),
            total_tax=round(total_tax, 3),
            avg_actual_cost=round(total_actual_cost / total_quantity, 3),
            image_url=instances[0].image,
            received_for_free=received_for_free,
        )

    def search_item(self, name: str, exact: bool = True) -> list[Item]:
        if exact:
            return [
                item for item in self.all_items if name.lower() == item.name.lower()
            ]
        else:
            return [
                item for item in self.all_items if name.lower() in item.name.lower()
            ]

    def _is_valid_id(self, item_id: int) -> bool:
        if item_id in self.items_map:
            return True
        raise ValueError(f"item with id = {repr(item_id)} does not exist.")

    def _get_attr_detail(self, attr: str) -> list[tuple[Any, int]]:
        return Counter(getattr(item, attr) for item in self.all_items).most_common()

    def _get_addons_detail(self) -> list[tuple[Any, int]]:
        return Counter(
            addon["name"] for item in self.all_items for addon in item.addons
        ).most_common()

    def _get_variants_detail(self) -> list[tuple[Any, int]]:
        return Counter(
            variant["name"] for item in self.all_items for variant in item.variants
        ).most_common()

    def _get_category_details(self) -> list[tuple[str, int]]:
        return Counter(
            item.category_details["category"] for item in self.all_items
        ).most_common()

    def _get_items_map(self) -> dict[int, list[Item]]:
        items = sorted(self.all_items, key=lambda x: x.item_id)
        return {item.item_id: list(grped_vals) for item, grped_vals in groupby(items)}
