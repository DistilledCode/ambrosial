from collections import Counter, defaultdict
from statistics import mean
from typing import Union

from swiggy import Swiggy
from swiggy.address import DeliveryAddress
from swiggy.order import Order


class AddressAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_orders = self.swiggy.order()
        self.all_addresses = self.swiggy.deliveryaddress()

    def groupby(self, attr: str = None) -> dict[Union[DeliveryAddress, str], int]:
        if attr is None:
            return dict(Counter(self.all_addresses).most_common())
        return dict(Counter(getattr(i, attr) for i in self.all_addresses).most_common())

    def coordinates(self):
        return [
            {
                "id_version": f"{address.id}_{address.version}",
                "annotation": address.annotation,
                "latitude": address.lat,
                "longitude": address.lng,
            }
            for address in set(self.all_addresses)
        ]

    def _get_key(self, order: Order, group_versions: bool):
        return (
            f"{order.delivery_address.id}_{order.delivery_address.version}"
            if group_versions
            else order.delivery_address.id
        )

    def history(self, group_versions: bool = True):
        hist = defaultdict(list)
        for order in self.all_orders:
            hist[self._get_key(order, group_versions)].append(
                {
                    "order_id": order.order_id,
                    "order_time": order.order_time,
                }
            )
        return dict(hist)

    def avg_delivery_time(self, group_versions: bool = False):
        del_time = defaultdict(list)
        for order in self.all_orders:
            del_time[self._get_key(order, group_versions)].append(
                order.delivery_time_in_seconds
            )
        return dict(
            {
                address: round(mean(total_dt), 4)
                for address, total_dt in del_time.items()
            }
        )
