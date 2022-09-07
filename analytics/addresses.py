from collections import Counter, defaultdict
from typing import Union

from swiggy import Swiggy
from swiggy.address import DeliveryAddress

from analytics import SwiggyAnalytics


class AddressAnalytics(SwiggyAnalytics):
    def __init__(self, swiggy: Swiggy = None) -> None:
        SwiggyAnalytics.__init__(self, swiggy)

    def most_common(self, attr: str = None) -> dict[Union[DeliveryAddress, str], int]:
        if attr is None:
            return dict(Counter(self.addresses).most_common())
        return dict(Counter(getattr(i, attr) for i in self.addresses).most_common())

    def coordinates(self):
        return [
            {
                "id_ver": f"{address.id}_{address.version}",
                "latitude": address.lat,
                "longitude": address.lng,
            }
            for address in set(self.addresses)
        ]

    def history(self, reverse: bool = False):
        hist = defaultdict(list)
        for order in self.orders:
            key = f"{order.delivery_address.id}_{order.delivery_address.version}"
            hist[key].append(
                {
                    "order_id": order.order_id,
                    "order_time": order.order_time,
                }
            )
        if reverse is True:
            for key in hist:
                hist[key].sort()
        return dict(hist)
